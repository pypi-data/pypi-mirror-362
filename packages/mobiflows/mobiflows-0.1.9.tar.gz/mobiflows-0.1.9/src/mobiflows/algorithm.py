# pyright: reportCallIssue=false, reportOperatorIssue=false, reportArgumentType=false, reportAttributeAccessIssue=false
# flake8: noqa: E501

from datetime import timedelta
from typing import Dict, List, Tuple

import geopandas as gpd
import numpy as np
import pandas as pd
import polars as pl


class CellTrajectory:
    def __init__(
        self,
        tdf: pl.DataFrame,
        v_id_col: str = "v_id",
        time_col: str = "datetime",
        uid_col: str = "uid",
        neighborhoods: Dict = {},
    ) -> None:
        """
        Parameters
        ----------
        tdf : pandas.DataFrame
            Trajectory data with columns [uid, datetime, longitude, latitude]
            with regular observations for every users (interval τ,
            a balanced panel)
        v_id_col : str, optional
            The name of the column in the data containing the cell ID
            (default is "v_id")
        time_col : str, optional
            Time column name (default "time")
        uid_col : str, optional
            User ID column name (default "uid")
        neighborhoods: Dict, optional
            Dictionary of neighbors for each cell in a user defined tessellation (default None)
        """

        super().__init__()
        self.v_id = v_id_col
        self.time = time_col
        self.uid = uid_col
        self.neighborhoods = neighborhoods

        if self.v_id not in tdf.columns:
            raise TypeError(
                "Cell trajectory dataframe does not contain cell IDs or cell IDs column does not match what was set."
            )
        if self.time not in tdf.columns:
            raise TypeError(
                "Cell trajectory dataframe does not contain a time column or time column does not match what was set."
            )
        if self.uid not in tdf.columns:
            raise TypeError(
                "Cell trajectory dataframe does not contain a uid column or uid column does not match what was set."
            )

        self.tdf = tdf.sort(by=[uid_col, time_col])

    def get_tdf(self) -> pl.DataFrame:
        """getter"""
        return self.tdf

    def set_neighborhoods(self, neighborhoods: Dict) -> None:
        """set neighborhoods

        Parameters
        ----------
        neighborhoods: Dictionary of neighbors for each cell in a user defined tessellation
        """

        self.neighborhoods = neighborhoods

    def build_neighborhoods(self, tessellation: gpd.GeoDataFrame, k: int = 1) -> Dict:
        """build neighborhoods

        Parameters
        ----------
        tessellation : geopandas.GeoDataFrame
            Tessellation, e.g., Voronoi tessellation and any nonoverlapping coverage
            tessellation with columns [v_id, longitude, latitude, geometry]
        k : int, optional
            Order of the neighborhoods (default "1")

        Returns
        -------
        Dict
            Dictionary of k-th order neighbors for each cell in the tessellation
        """

        if k < 0:
            raise ValueError("k cannot be zero.")

        v_id_type = self.tdf.schema[self.v_id]
        v_type = "str" if v_id_type == pl.String else v_id_type
        tessellation[self.v_id] = tessellation[self.v_id].astype(v_type)

        sindex = tessellation.sindex

        cell_ids = tessellation[self.v_id].to_list()
        n = len(cell_ids)
        N = np.eye(n, dtype=int)
        idx_to_id = {i: cell_id for i, cell_id in enumerate(cell_ids)}
        if k > 0:
            id_to_idx = {cell_id: i for i, cell_id in enumerate(cell_ids)}
            A = np.zeros((n, n), dtype=int)

            for idx, geom in zip(cell_ids, tessellation.geometry):

                ids = list(sindex.intersection(geom.bounds))
                nei = tessellation.iloc[ids]

                # true neighbors are those that really touch the geometry
                neighbors = nei.loc[nei.geometry.touches(geom)][self.v_id].tolist()

                i = id_to_idx[idx]

                for neighbor_id in neighbors:
                    j = id_to_idx[neighbor_id]
                    A[i, j] = 1

            # to make sure that A is symmetric
            A = np.maximum(A, A.T)

            N = (np.linalg.matrix_power(A, k) > 0).astype(int)
            np.fill_diagonal(N, 1)

        neighborhoods = {
            idx_to_id[i]: set([idx_to_id[j] for j in np.flatnonzero(N[i])])
            for i in range(n)
        }
        return neighborhoods

    def _stayers(self, tau: int = 30, w: int = 60) -> Tuple[pl.DataFrame, pl.DataFrame]:
        """compute stayers

        Parameters
        ----------
        tau : int
            Time resolution of data in minutes
            (default is 30 minutes)
        w : int
            Duration at a location used to define a trip in minutes
            (default is 60 minutes, must be a multiple of tau)

        Returns
        -------
        Tuple[polars.DataFrame, polars.DataFrame]
            First polars dataframe with the columns
            [uid, v_id, time] are stayers.
            The second polars dataframe contains the number of stayers at each
            possible stay time period
        """

        if w % tau != 0:
            raise ValueError("w must be a multiple of tau.")

        if not self.neighborhoods:
            raise ValueError(
                "please set neighborhoods for this object. Use the method `set_neighborhoods`."
            )

        tdf = self.tdf.sort([self.uid, self.time])
        d = w // tau + 1

        def detect_stays(df: pl.DataFrame) -> pl.DataFrame:
            n_rows = df.height
            if n_rows < d:
                return pl.DataFrame(
                    schema=[
                        (self.uid, pl.Int64),
                        (self.v_id, df.schema[self.v_id]),
                        (self.time, pl.Datetime),
                    ]
                )

            shifted = df
            for i in range(d - 1, -1, -1):
                shifted = shifted.with_columns(
                    pl.col(self.v_id).shift(i).alias(f"lag_{i}")
                )

            shifted = shifted.slice(d - 1, n_rows - (d - 1))
            stay_rows = []

            for row in shifted.iter_rows(named=True):
                t = row[self.time]
                positions = [row[f"lag_{i}"] for i in range(d)]
                current_cell = row[self.v_id]
                neighbors_of_current = self.neighborhoods.get(current_cell, set())

                for v_q in neighbors_of_current:
                    neighbors_set = self.neighborhoods[v_q]

                    # condition 1: all cells in window inside N(v_q)
                    if all(cell in neighbors_set for cell in positions):
                        count_vq = sum(cell == v_q for cell in positions)

                        # condition 2: majority condition
                        if count_vq > (d / 2):
                            stay_rows.append(
                                {self.uid: row[self.uid], self.v_id: v_q, self.time: t}
                            )
            if stay_rows:
                return pl.DataFrame(stay_rows)
            else:
                return pl.DataFrame(
                    schema=[
                        (self.uid, pl.Int64),
                        (self.v_id, df.schema[self.v_id]),
                        (self.time, pl.Datetime),
                    ]
                )

        stayers = tdf.group_by(self.uid, maintain_order=True).map_groups(detect_stays)

        min_time = self.tdf[self.time].min()
        max_time = self.tdf[self.time].max()
        stay_start = min_time + (d - 1) * timedelta(minutes=tau)
        time_range = pl.datetime_range(
            start=stay_start, end=max_time, interval=f"{tau}m", eager=True
        ).sort()
        v_ids = self.tdf[self.v_id].unique().to_list()
        n_stayers = pl.DataFrame(
            {
                self.v_id: v_ids * len(time_range),
                self.time: np.repeat(time_range, len(v_ids)),
            }
        )

        n_stayers = (
            n_stayers.join(
                stayers.group_by([self.v_id, self.time]).agg(n_stayers=pl.len()),
                on=[self.v_id, self.time],
                how="left",
            )
            .with_columns(pl.col("n_stayers").fill_null(0))
            .sort([self.v_id, self.time])
        )

        return stayers, n_stayers

    def _leavers(self, stayers: pl.DataFrame, tau: int = 30) -> pl.DataFrame:
        """leavers

        Parameters
        ----------
        stayers : pl.DataFrame
            Stayers dataframe with columns [uid, v_id, datetime]
        tau : int
            Time resolution of data in minutes
            (default is 30 minutes)

        Returns
        -------
        polars.DataFrame
            Leavers [uid, origin, leave_time]
        """

        if not self.neighborhoods:
            raise ValueError(
                "please set neighborhoods for this object. Use the method `set_neighborhoods`."
            )

        stayers = stayers.with_columns(
            neighbors=pl.col(self.v_id).map_elements(
                lambda vid: list(self.neighborhoods.get(vid, [])),
                return_dtype=pl.List(stayers.schema[self.v_id]),
            )
        )

        stayers = stayers.with_columns(
            next_stay_time=pl.col(self.time).shift(-1).over(self.uid),
            next_time=pl.col(self.time) + pl.duration(minutes=tau),
        ).filter(pl.col("next_stay_time").is_not_null())

        leavers = (
            stayers.join(
                self.tdf,
                left_on=[self.uid, "next_time"],
                right_on=[self.uid, self.time],
                suffix="_next",
                how="left",
            )
            .filter(~pl.col(f"{self.v_id}_next").is_in(pl.col("neighbors")))
            .select(
                [
                    pl.col(self.uid),
                    pl.col(self.v_id).alias("origin"),
                    pl.col(self.time).alias("leave_time"),
                ]
            )
        )

        return leavers

    def _movers(self, stayers: pl.DataFrame, leavers: pl.DataFrame) -> pl.DataFrame:
        """leavers

        Parameters
        ----------
        stayers : pl.DataFrame
            Stayers dataframe with columns [uid, v_id, datetime]
        leavers : pl.DataFrame
            Leavers dataframe with columns [uid, origin, leave_time]

        Returns
        -------
        polars.DataFrame
            Movers [uid, origin, dest, leave_time, arrival_time],
            where leave_time is the origin leave time and arrival_time
            is the time of arrival at the destination
        """

        stayers = stayers.rename({self.v_id: "dest", self.time: "stay_time"})
        movers = leavers.join(stayers, on=self.uid, how="inner")
        # t' > t
        movers = movers.filter(pl.col("stay_time") > pl.col("leave_time"))
        # no intermediate stays between t and t'
        # (i.e., no intermediate stay_time)
        first_arrival = movers.group_by([self.uid, "origin", "leave_time"]).agg(
            arrival_time=pl.col("stay_time").min()
        )

        first_arrival = first_arrival.join(
            stayers,
            left_on=[self.uid, "arrival_time"],
            right_on=[self.uid, "stay_time"],
            how="inner",
        )
        movers = first_arrival.select(
            [
                self.uid,
                "origin",
                "dest",
                "leave_time",
                "arrival_time",
            ]
        )

        return movers

    def build_cell_flows(
        self, tau: int = 30, w: int = 60, self_loops: bool = True
    ) -> Tuple[pl.DataFrame, pl.DataFrame]:
        """build cell flows

        Parameters
        ----------
        tau : int
            Time resolution of data in minutes
            (default is 30 minutes)
        w : int
            Duration at a location used to define a trip in minutes
            (default is 60 minutes, must be a multiple of tau)

        Returns
        -------
        Tuple[polars.DataFrame, polars.DataFrame]
            First polars dataframe with the columns
            [origin, dest, time] are flows between cells.
            The second polars dataframe contains the number of stayers at each
            possible stay time period
        """

        if w % tau != 0:
            raise ValueError("w must be a multiple of tau.")

        stayers, n_stayers = self._stayers(tau, w)
        leavers = self._leavers(stayers, tau)
        movers = self._movers(stayers, leavers)

        movers = movers.with_columns(time=pl.col("leave_time"))
        v_flows = (
            movers.group_by(["origin", "dest", "time"])
            .agg(count=pl.len())
            .sort(["origin", "dest", "time"])
        )

        # remove self-loops at the cell level
        if not self_loops:
            v_flows = v_flows.filter(pl.col("origin") != pl.col("dest"))

        return v_flows, n_stayers

    def build_zipcode_flows(
        self,
        cell_flows: pl.DataFrame,
        cell_stayers: pl.DataFrame,
        cell_zipcode_intersection_proportions: pl.DataFrame,
        postcodes: List[int],
        tau: int = 30,
        self_loops: bool = False,
    ) -> pl.DataFrame:
        """build zipcode flows

        Parameters
        ----------
        cell_flows : polars.DataFrame
            Cell Flows (e.g. flows between voronoi cells)
        cell_stayers : polars.DataFrame
            Number of stayers at each possible stay time period
        cell_zipcode_intersection_proportions : polars.DataFrame
            Proportion of intersection between cells and zipcodes
            with columns [pcode, v_id, p], where p is the proportion
            of intersection of the pcode and cell (v_id). pcodes are integers
        postcodes : List[int]
            List of postcodes
        tau : int
            Time resolution of data in minutes
            (default is 30 minutes)
        self_loops : bool
            To remove or not to remove loops (default is False)

        Returns
        -------
        polars.DataFrame
            Polars dataframe with the columns
            [origin, dest, time, n_origin]
        """

        cell_stayers = (
            cell_stayers.join(
                cell_zipcode_intersection_proportions,
                on=self.v_id,
                suffix="_origin",
                how="left",
                coalesce=True,
            )
            .rename({"pcode": "origin"})
            .with_columns(np=((pl.col("n_stayers") * pl.col("p"))))
            .group_by([self.time, "origin"])
            .agg(count_avg=pl.sum("np"))
            .with_columns(n_origin=(((pl.col("count_avg")))))
            .select(["origin", self.time, "n_origin"])
            .sort(["origin", self.time])
        )

        flows = (
            (
                cell_flows.join(
                    cell_zipcode_intersection_proportions,
                    left_on="origin",
                    right_on="v_id",
                    suffix="_origin",
                    how="left",
                )
                .join(
                    cell_zipcode_intersection_proportions,
                    left_on="dest",
                    right_on="v_id",
                    suffix="_dest",
                    how="left",
                )
                .rename({"p": "p_origin", "pcode": "pcode_origin"})
                .with_columns(p=pl.col("p_origin") * pl.col("p_dest"))
                .with_columns(count_avg=pl.col("p") * pl.col("count"))
                .select(
                    origin=pl.col("pcode_origin"),
                    dest=pl.col("pcode_dest"),
                    time=pl.col("time"),
                    p=pl.col("p"),
                    count_avg=pl.col("count_avg"),
                )
            )
            .group_by(["origin", "dest", "time"])
            .agg(count_avg=pl.sum("count_avg"))
            .with_columns(count=pl.col("count_avg"))
            .select(["origin", "dest", "time", "count"])
        )

        flows_start = cell_flows["time"].min()
        flows_end = cell_flows["time"].max()

        time_range = pl.datetime_range(
            start=flows_start, end=flows_end, interval=f"{tau}m", eager=True
        ).sort()

        # structural zero flows
        df = pl.DataFrame(
            dict(
                origin=np.repeat(postcodes, len(postcodes) * len(time_range)),
                dest=postcodes * len(postcodes) * len(time_range),
                time=np.repeat(time_range.to_list(), len(postcodes)).tolist()
                * len(postcodes),
            ),
            schema={"origin": pl.Int64, "dest": pl.Int64, "time": pl.Datetime},
        )

        flows = df.join(flows, on=["origin", "dest", "time"], how="left", coalesce=True)
        flows = flows.with_columns(pl.col("count").fill_null(0))

        flows = flows.join(
            cell_stayers,
            left_on=["origin", "time"],
            right_on=["origin", self.time],
            how="left",
        ).sort(["origin", "dest", "time"])

        if not self_loops:
            flows = flows.filter(pl.col("origin") != pl.col("dest"))

        return flows


class Trajectory(pl.DataFrame):
    def __init__(
        self,
        tdf: pl.DataFrame,
        longitude: str = "lon",
        latitude: str = "lat",
        v_id_col: str = "v_id",
        time_col: str = "datetime",
        uid_col: str = "uid",
    ) -> None:
        """
        Parameters
        ----------
        tdf : pandas.DataFrame
            Trajectory data with columns [uid, datetime, longitude, latitude]
            with regular observations for every users (interval τ,
            a balanced panel)
        longitude : str, optional
            The name of the column in the data containing the longitude
            (default is "lon")
        latitude : str, optional
            The name of the column in the data containing the latitude
            (default is "lat")
        v_id_col : str, optional
            Column identifying tile IDs in the tessellation dataframe
            (default is "v_id")
        time_col : str, optional
            Time column name (default "time")
        uid_col : str, optional
            User ID column name (default "uid")
        """

        super().__init__()
        self.lon = longitude
        self.lat = latitude
        self.v_id = v_id_col
        self.time = time_col
        self.uid = uid_col

        if self.lon not in tdf.columns:
            raise TypeError(
                "Cell trajectory dataframe does not contain a longitude column or the longitude column does not match what was set."
            )
        if self.lat not in tdf.columns:
            raise TypeError(
                "Cell trajectory dataframe does not contain a latitude column or the latitude column does not match what was set."
            )

        if self.time not in tdf.columns:
            raise TypeError(
                "Cell trajectory dataframe does not contain a time column or time column does not match what was set."
            )
        if self.uid not in tdf.columns:
            raise TypeError(
                "Cell trajectory dataframe does not contain a uid column or uid column does not match what was set."
            )

        self.tdf = tdf.sort(by=[uid_col, time_col])

    def mapping(self, tessellation: gpd.GeoDataFrame) -> CellTrajectory:
        """Map (pseudo-)locations to coverage cells

        Parameters
        ----------
        tessellation : geopandas.GeoDataFrame
            Tessellation, e.g., Voronoi tessellation and any coverage
            tessellation with columns [v_id, longitude, latitude, geometry]

        Returns
        -------
        polars.DataFrame
            Polars dataframe with the columns
            [uid, datetime, longitude, latitude, v_id]
        """

        if self.v_id not in tessellation.columns:
            raise TypeError(
                "Cell trajectory dataframe does not contain cell IDs or cell IDs column does not match what was set."
            )

        gdf = gpd.GeoDataFrame(
            self.tdf.to_pandas(),
            geometry=gpd.points_from_xy(self.tdf[self.lon], self.tdf[self.lat]),
            crs=tessellation.crs,
        )
        joined = gpd.sjoin(
            gdf, tessellation[[self.v_id, "geometry"]], how="left", predicate="within"
        )
        gdf[self.v_id] = joined[self.v_id]

        matched = gdf[~gdf[self.v_id].isna()]
        unmatched = gdf[gdf[self.v_id].isna()].copy()

        if not unmatched.empty:
            # build a lookup of future assigned regions per user
            tessellation = tessellation.copy()
            tessellation["rep"] = gpd.points_from_xy(
                tessellation[self.lon], tessellation[self.lat]
            )

            matched_sorted = matched.sort_values(by=[self.uid, self.time])
            future_region_lookup = matched_sorted.groupby(self.uid).apply(
                lambda df: df.set_index(self.time)[self.v_id], include_groups=False
            )

            # find candidate cells for all unmatched points (intersection test)
            unmatched["candidates"] = unmatched.geometry.apply(
                lambda geom: tessellation[tessellation.geometry.intersects(geom)][
                    [self.v_id, "rep"]
                ]
            )

            fallback_ids = []
            for _, row in unmatched.iterrows():
                uid = row[self.uid]
                time = row[self.time]

                # candidate cells at current time
                candidates = row["candidates"]
                if candidates.empty:
                    raise ValueError(
                        f"""tdf not proper: trajectory point for user {uid} at time
                            {time} intersects no tessellation cell."""
                    )

                # find user's next assigned cell
                if uid not in future_region_lookup:
                    raise ValueError(
                        f"""tdf not proper: uid {uid} does not have any point
                            assigned to a cell to a cell."""
                    )

                user_future = future_region_lookup[uid]
                future_times = user_future[user_future.index > time]

                if future_times.empty:
                    raise ValueError(
                        f"""tdf not proper: no future point for uid {uid} at time
                            {time}."""
                    )

                future_id = future_times.iloc[0]
                future_geom = tessellation.loc[
                    tessellation[self.v_id] == future_id, "rep"
                ].values[0]

                # choose closest candidate cell to the future one
                candidates["dist"] = candidates["rep"].distance(future_geom)
                fallback_id = candidates.sort_values(by="dist").iloc[0][self.v_id]
                fallback_ids.append(fallback_id)

            unmatched[self.v_id] = fallback_ids

            gdf = pd.concat(
                [matched, unmatched.drop(columns=["candidates"])], ignore_index=True
            )

        gdf.drop(columns=[self.lon, self.lat, "geometry"], inplace=True)

        return CellTrajectory(pl.DataFrame(gdf.sort_values(by=[self.uid, self.time])))
