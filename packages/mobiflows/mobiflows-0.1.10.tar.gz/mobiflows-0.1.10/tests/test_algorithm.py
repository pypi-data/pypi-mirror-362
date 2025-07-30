# pyright: reportCallIssue=false
# flake8: noqa: E501

from datetime import datetime

import geopandas as gpd
import polars as pl
import pytest
import shapely as sp

from mobiflows.algorithm import CellTrajectory, Trajectory

TDF = pl.DataFrame(
    dict(
        uid=[
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            2,
            2,
            2,
            2,
            2,
            2,
            2,
            2,
            2,
            2,
            2,
            2,
            3,
            3,
            3,
            3,
            3,
            3,
            3,
            3,
            3,
            3,
            3,
            3,
            4,
            4,
            4,
            4,
            4,
            4,
            4,
            4,
            4,
            4,
            4,
            4,
            5,
            5,
            5,
            5,
            5,
            5,
            5,
            5,
            5,
            5,
            5,
            5,
        ],
        datetime=[
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            10,
            11,
            12,
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            10,
            11,
            12,
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            10,
            11,
            12,
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            10,
            11,
            12,
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            10,
            11,
            12,
        ],
        lon=[
            0,
            0,
            0,
            0,
            1,
            1,
            1,
            1,
            1,
            0,
            0,
            0,
            0,
            0,
            0,
            2,
            3,
            2,
            0,
            0,
            0,
            1,
            1,
            1,
            3,
            3,
            3,
            2,
            1,
            0,
            0,
            0,
            0,
            0,
            1,
            2,
            0,
            0,
            0,
            3,
            3,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
        ],
        lat=[
            0,
            0,
            0,
            1,
            1,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            1,
            1,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            3,
            3,
            3,
            3,
            3,
            3,
            2,
            2,
            2,
            2,
            2,
            2,
            0,
            0,
            0,
            2,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
        ],
        v_id=[
            "0",
            "0",
            "0",
            "1",
            "5",
            "4",
            "4",
            "4",
            "4",
            "0",
            "0",
            "0",
            "0",
            "0",
            "0",
            "9",
            "13",
            "8",
            "0",
            "0",
            "0",
            "4",
            "4",
            "4",
            "15",
            "15",
            "15",
            "11",
            "7",
            "3",
            "2",
            "2",
            "2",
            "2",
            "6",
            "10",
            "0",
            "0",
            "0",
            "14",
            "12",
            "4",
            "4",
            "4",
            "4",
            "4",
            "4",
            "4",
            "0",
            "0",
            "0",
            "0",
            "0",
            "0",
            "0",
            "0",
            "0",
            "0",
            "0",
            "0",
        ],
    )
)

POINTS = sp.MultiPoint(
    [
        [0, 0],
        [0, 1],
        [0, 2],
        [0, 3],
        [1, 0],
        [1, 1],
        [1, 2],
        [1, 3],
        [2, 0],
        [2, 1],
        [2, 2],
        [2, 3],
        [3, 0],
        [3, 1],
        [3, 2],
        [3, 3],
    ]
)
V = sp.voronoi_polygons(POINTS)
SORTED_V = sorted(V.geoms, key=lambda p: (p.centroid.x, p.centroid.y))

POINT_LIST = list(POINTS.geoms)
TESSELLATION = gpd.GeoDataFrame(
    dict(
        v_id=[str(i) for i in range(len(SORTED_V))],
        lon=[pt.x for pt in POINT_LIST],
        lat=[pt.y for pt in POINT_LIST],
        geometry=list(SORTED_V),
    ),
    crs=4326,
)


def test_mapping():
    tdf = Trajectory(
        pl.DataFrame(
            dict(
                uid=[
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                    2,
                    2,
                    2,
                    2,
                    2,
                    2,
                    3,
                    3,
                    3,
                    3,
                    3,
                    3,
                    4,
                    4,
                    4,
                    4,
                    4,
                    4,
                    5,
                    5,
                    5,
                    5,
                    5,
                    5,
                ],
                datetime=[
                    1,
                    2,
                    3,
                    4,
                    5,
                    6,
                    1,
                    2,
                    3,
                    4,
                    5,
                    6,
                    1,
                    2,
                    3,
                    4,
                    5,
                    6,
                    1,
                    2,
                    3,
                    4,
                    5,
                    6,
                    1,
                    2,
                    3,
                    4,
                    5,
                    6,
                ],
                lon=[
                    0.0,
                    0.0,
                    0.5,
                    1.5,
                    2.0,
                    2.0,
                    2.0,
                    1.5,
                    1.5,
                    0.5,
                    0.5,
                    0.0,
                    0.0,
                    0.5,
                    1.0,
                    1.5,
                    1.5,
                    2.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    1.0,
                    1.0,
                    1.0,
                    1.0,
                    1.0,
                    1.0,
                ],
                lat=[
                    0.0,
                    0.0,
                    0.5,
                    1.5,
                    2.0,
                    2.0,
                    0.0,
                    0.5,
                    0.5,
                    1.5,
                    1.5,
                    2.0,
                    1.0,
                    1.0,
                    1.0,
                    1.0,
                    1.0,
                    1.0,
                    0.0,
                    0.0,
                    1.0,
                    1.0,
                    2.0,
                    2.0,
                    0.0,
                    0.5,
                    0.0,
                    1.0,
                    1.5,
                    2.0,
                ],
            )
        )
    )

    true_mapped_tdf = pl.DataFrame(
        dict(
            uid=[
                1,
                1,
                1,
                1,
                1,
                1,
                2,
                2,
                2,
                2,
                2,
                2,
                3,
                3,
                3,
                3,
                3,
                3,
                4,
                4,
                4,
                4,
                4,
                4,
                5,
                5,
                5,
                5,
                5,
                5,
            ],
            datetime=[
                1,
                2,
                3,
                4,
                5,
                6,
                1,
                2,
                3,
                4,
                5,
                6,
                1,
                2,
                3,
                4,
                5,
                6,
                1,
                2,
                3,
                4,
                5,
                6,
                1,
                2,
                3,
                4,
                5,
                6,
            ],
            v_id=[
                "0",
                "0",
                "5",
                "10",
                "10",
                "10",
                "8",
                "5",
                "5",
                "2",
                "2",
                "2",
                "1",
                "5",
                "5",
                "9",
                "9",
                "9",
                "0",
                "0",
                "1",
                "1",
                "2",
                "2",
                "4",
                "4",
                "4",
                "5",
                "6",
                "6",
            ],
        )
    )

    mapped_tdf = tdf.mapping(TESSELLATION).get_tdf()
    assert true_mapped_tdf.equals(mapped_tdf)


def test_build_neighborhoods():
    true_first_order_neighborhoods = {
        "0": set(["0", "1", "4", "5"]),
        "1": set(["0", "1", "2", "4", "5", "6"]),
        "2": set(["1", "2", "3", "5", "6", "7"]),
        "3": set(["2", "3", "6", "7"]),
        "4": set(["0", "1", "4", "5", "8", "9"]),
        "5": set(["0", "1", "2", "4", "5", "6", "8", "9", "10"]),
        "6": set(["1", "2", "3", "5", "6", "7", "9", "10", "11"]),
        "7": set(["2", "3", "6", "7", "10", "11"]),
        "8": set(["4", "5", "8", "9", "12", "13"]),
        "9": set(["4", "5", "6", "8", "9", "10", "12", "13", "14"]),
        "10": set(["5", "6", "7", "9", "10", "11", "13", "14", "15"]),
        "11": set(["6", "7", "10", "11", "14", "15"]),
        "12": set(["8", "9", "12", "13"]),
        "13": set(["8", "9", "10", "12", "13", "14"]),
        "14": set(["9", "10", "11", "13", "14", "15"]),
        "15": set(["10", "11", "14", "15"]),
    }
    true_second_order_neighborhoods = {
        "0": set(["0", "1", "2", "4", "5", "6", "8", "9", "10"]),
        "1": set(["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"]),
        "2": set(["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"]),
        "3": set(["1", "2", "3", "5", "6", "7", "9", "10", "11"]),
        "4": set(["0", "1", "2", "4", "5", "6", "8", "9", "10", "12", "13", "14"]),
        "5": set(
            [
                "0",
                "1",
                "2",
                "3",
                "4",
                "5",
                "6",
                "7",
                "8",
                "9",
                "10",
                "11",
                "12",
                "13",
                "14",
                "15",
            ]
        ),
        "6": set(
            [
                "0",
                "1",
                "2",
                "3",
                "4",
                "5",
                "6",
                "7",
                "8",
                "9",
                "10",
                "11",
                "12",
                "13",
                "14",
                "15",
            ]
        ),
        "7": set(["1", "2", "3", "5", "6", "7", "9", "10", "11", "13", "14", "15"]),
        "8": set(["0", "1", "2", "4", "5", "6", "8", "9", "10", "12", "13", "14"]),
        "9": set(
            [
                "0",
                "1",
                "2",
                "3",
                "4",
                "5",
                "6",
                "7",
                "8",
                "9",
                "10",
                "11",
                "12",
                "13",
                "14",
                "15",
            ]
        ),
        "10": set(
            [
                "0",
                "1",
                "2",
                "3",
                "4",
                "5",
                "6",
                "7",
                "8",
                "9",
                "10",
                "11",
                "12",
                "13",
                "14",
                "15",
            ]
        ),
        "11": set(["1", "2", "3", "5", "6", "7", "9", "10", "11", "13", "14", "15"]),
        "12": set(["4", "5", "6", "8", "9", "10", "12", "13", "14"]),
        "13": set(["4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15"]),
        "14": set(["4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15"]),
        "15": set(["5", "6", "7", "9", "10", "11", "13", "14", "15"]),
    }

    true_third_order_neighborhoods = {
        "0": set(
            [
                "0",
                "1",
                "2",
                "3",
                "4",
                "5",
                "6",
                "7",
                "8",
                "9",
                "10",
                "11",
                "12",
                "13",
                "14",
                "15",
            ]
        ),
        "1": set(
            [
                "0",
                "1",
                "2",
                "3",
                "4",
                "5",
                "6",
                "7",
                "8",
                "9",
                "10",
                "11",
                "12",
                "13",
                "14",
                "15",
            ]
        ),
        "2": set(
            [
                "0",
                "1",
                "2",
                "3",
                "4",
                "5",
                "6",
                "7",
                "8",
                "9",
                "10",
                "11",
                "12",
                "13",
                "14",
                "15",
            ]
        ),
        "3": set(
            [
                "0",
                "1",
                "2",
                "3",
                "4",
                "5",
                "6",
                "7",
                "8",
                "9",
                "10",
                "11",
                "12",
                "13",
                "14",
                "15",
            ]
        ),
        "4": set(
            [
                "0",
                "1",
                "2",
                "3",
                "4",
                "5",
                "6",
                "7",
                "8",
                "9",
                "10",
                "11",
                "12",
                "13",
                "14",
                "15",
            ]
        ),
        "5": set(
            [
                "0",
                "1",
                "2",
                "3",
                "4",
                "5",
                "6",
                "7",
                "8",
                "9",
                "10",
                "11",
                "12",
                "13",
                "14",
                "15",
            ]
        ),
        "6": set(
            [
                "0",
                "1",
                "2",
                "3",
                "4",
                "5",
                "6",
                "7",
                "8",
                "9",
                "10",
                "11",
                "12",
                "13",
                "14",
                "15",
            ]
        ),
        "7": set(
            [
                "0",
                "1",
                "2",
                "3",
                "4",
                "5",
                "6",
                "7",
                "8",
                "9",
                "10",
                "11",
                "12",
                "13",
                "14",
                "15",
            ]
        ),
        "8": set(
            [
                "0",
                "1",
                "2",
                "3",
                "4",
                "5",
                "6",
                "7",
                "8",
                "9",
                "10",
                "11",
                "12",
                "13",
                "14",
                "15",
            ]
        ),
        "9": set(
            [
                "0",
                "1",
                "2",
                "3",
                "4",
                "5",
                "6",
                "7",
                "8",
                "9",
                "10",
                "11",
                "12",
                "13",
                "14",
                "15",
            ]
        ),
        "10": set(
            [
                "0",
                "1",
                "2",
                "3",
                "4",
                "5",
                "6",
                "7",
                "8",
                "9",
                "10",
                "11",
                "12",
                "13",
                "14",
                "15",
            ]
        ),
        "11": set(
            [
                "0",
                "1",
                "2",
                "3",
                "4",
                "5",
                "6",
                "7",
                "8",
                "9",
                "10",
                "11",
                "12",
                "13",
                "14",
                "15",
            ]
        ),
        "12": set(
            [
                "0",
                "1",
                "2",
                "3",
                "4",
                "5",
                "6",
                "7",
                "8",
                "9",
                "10",
                "11",
                "12",
                "13",
                "14",
                "15",
            ]
        ),
        "13": set(
            [
                "0",
                "1",
                "2",
                "3",
                "4",
                "5",
                "6",
                "7",
                "8",
                "9",
                "10",
                "11",
                "12",
                "13",
                "14",
                "15",
            ]
        ),
        "14": set(
            [
                "0",
                "1",
                "2",
                "3",
                "4",
                "5",
                "6",
                "7",
                "8",
                "9",
                "10",
                "11",
                "12",
                "13",
                "14",
                "15",
            ]
        ),
        "15": set(
            [
                "0",
                "1",
                "2",
                "3",
                "4",
                "5",
                "6",
                "7",
                "8",
                "9",
                "10",
                "11",
                "12",
                "13",
                "14",
                "15",
            ],
        ),
    }

    trajectory = CellTrajectory(TDF)
    trajectory.set_neighborhoods(trajectory.build_neighborhoods(TESSELLATION, k=1))
    assert true_first_order_neighborhoods == trajectory.neighborhoods

    trajectory.set_neighborhoods(trajectory.build_neighborhoods(TESSELLATION, k=2))
    assert true_second_order_neighborhoods == trajectory.neighborhoods

    trajectory.set_neighborhoods(trajectory.build_neighborhoods(TESSELLATION, k=3))
    assert true_third_order_neighborhoods == trajectory.neighborhoods


def test_build_cell_flows():
    true_voronoi_flows_k_0 = pl.DataFrame(
        dict(
            origin=["0", "0", "15", "4", "0"],
            dest=["0", "4", "2", "0", "4"],
            time=[3, 3, 3, 9, 9],
            count=[1, 2, 1, 1, 1],
        )
    ).sort(by=["time", "origin", "dest"])

    true_voronoi_flows_k_1 = pl.DataFrame(
        dict(
            origin=["0", "0", "15"],
            dest=["0", "4", "2"],
            time=[3, 3, 4],
            count=[1, 1, 1],
        )
    ).sort(by=["time", "origin", "dest"])

    true_n_stayers_k_0 = pl.DataFrame(
        dict(
            v_id=[
                "0",
                "0",
                "0",
                "0",
                "0",
                "0",
                "0",
                "0",
                "0",
                "0",
                "4",
                "4",
                "4",
                "4",
                "4",
                "2",
                "2",
                "15",
            ],
            datetime=[3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 8, 9, 10, 11, 12, 9, 10, 3],
            n_stayers=[4, 1, 1, 1, 1, 1, 2, 1, 1, 2, 2, 2, 1, 1, 2, 1, 1, 1],
        )
    ).sort(["v_id", "datetime"])

    true_n_stayers_k_1 = pl.DataFrame(
        dict(
            v_id=[
                "0",
                "0",
                "0",
                "0",
                "0",
                "0",
                "0",
                "0",
                "0",
                "0",
                "2",
                "2",
                "2",
                "2",
                "4",
                "4",
                "4",
                "4",
                "4",
                "4",
                "15",
                "15",
            ],
            datetime=[
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                8,
                9,
                10,
                11,
                7,
                8,
                9,
                10,
                11,
                12,
                3,
                4,
            ],
            n_stayers=[
                4,
                2,
                1,
                1,
                1,
                1,
                2,
                2,
                2,
                2,
                1,
                1,
                1,
                1,
                1,
                2,
                2,
                2,
                2,
                2,
                1,
                1,
            ],
        )
    ).sort(["v_id", "datetime"])

    base_time = datetime(2025, 1, 1, 0, 0, 0)
    us = 30 * 60_000_000
    tdf = TDF.with_columns(
        datetime=pl.lit(base_time)
        + pl.col("datetime") * pl.lit(us).cast(pl.Duration("us"))
    )
    trajectory = CellTrajectory(tdf)
    trajectory.set_neighborhoods(trajectory.build_neighborhoods(TESSELLATION, k=0))

    with pytest.raises(ValueError) as val_err:
        v_flows = (
            trajectory.build_cell_flows(tau=30, w=40)[0]
            .with_columns(
                time=((pl.col("time") - pl.lit(base_time)) / us).cast(pl.Int64)
            )
            .sort(by=["time", "origin", "dest"])
        )
    assert "w must be a multiple of tau." in str(val_err.value)

    v_flows, n_stayers_k_0 = trajectory.build_cell_flows(tau=30, w=60)
    v_flows = v_flows.with_columns(
        time=((pl.col("time") - pl.lit(base_time)) / us).cast(pl.Int64)
    ).sort(by=["time", "origin", "dest"])
    assert true_voronoi_flows_k_0.equals(v_flows)

    n_stayers_k_0 = (
        n_stayers_k_0.filter(pl.col("n_stayers") > 0)
        .with_columns(
            datetime=((pl.col("datetime") - pl.lit(base_time)) / us).cast(pl.Int64)
        )
        .sort(["v_id", "datetime"])
    )
    assert true_n_stayers_k_0.equals(n_stayers_k_0)

    # set order of neighborhood k to 1
    trajectory.set_neighborhoods(trajectory.build_neighborhoods(TESSELLATION, k=1))
    v_flows, n_stayers_k_1 = trajectory.build_cell_flows(tau=30, w=60)
    v_flows = v_flows.with_columns(
        time=((pl.col("time") - pl.lit(base_time)) / us).cast(pl.Int64)
    ).sort(by=["time", "origin", "dest"])
    assert true_voronoi_flows_k_1.equals(v_flows)

    n_stayers_k_1 = (
        n_stayers_k_1.filter(pl.col("n_stayers") > 0)
        .with_columns(
            datetime=((pl.col("datetime") - pl.lit(base_time)) / us).cast(pl.Int64)
        )
        .sort(["v_id", "datetime"])
    )
    assert true_n_stayers_k_1.equals(n_stayers_k_1)


def test_build_zipcode_flows():
    true_flows_k_0 = pl.DataFrame(
        dict(
            origin=[1, 1, 3, 1, 1, 2],
            dest=[1, 2, 2, 1, 2, 1],
            time=[3, 3, 3, 9, 9, 9],
            count=[2.0, 1.0, 1.0, 1.0, 0.5, 0.5],
            n_origin=[4.0, 4.0, 1.0, 3.0, 3.0, 2.0],
        )
    ).sort(by=["origin", "dest", "time"])
    true_flows_k_1 = pl.DataFrame(
        dict(
            origin=[1, 1, 3],
            dest=[1, 2, 2],
            time=[3, 3, 4],
            count=[1.5, 0.5, 1.0],
            n_origin=[4.0, 4.0, 1.0],
        )
    ).sort(by=["origin", "dest", "time"])
    voronoi_zipcode_intersection_proportions = pl.DataFrame(
        dict(
            pcode=[1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3],
            v_id=[
                "0",
                "1",
                "4",
                "5",
                "6",
                "1",
                "2",
                "4",
                "6",
                "8",
                "9",
                "10",
                "3",
                "7",
                "11",
                "12",
                "13",
                "14",
                "15",
            ],
            p=[
                1.0,
                0.2,
                0.5,
                1.0,
                0.4,
                0.8,
                1.0,
                0.5,
                0.6,
                1.0,
                1.0,
                1.0,
                1.0,
                1.0,
                1.0,
                1.0,
                1.0,
                1.0,
                1.0,
            ],
        )
    )

    base_time = datetime(2025, 1, 1, 0, 0, 0)
    us = 60_000_000
    tdf = TDF.with_columns(
        datetime=pl.lit(base_time)
        + pl.col("datetime") * pl.lit(us).cast(pl.Duration("us"))
    )
    trajectory = CellTrajectory(tdf)
    trajectory.set_neighborhoods(trajectory.build_neighborhoods(TESSELLATION, k=0))

    v_flows_k_0, v_stayers_k_0 = trajectory.build_cell_flows(tau=1, w=2)
    flows_k_0 = (
        trajectory.build_zipcode_flows(
            v_flows_k_0,
            v_stayers_k_0,
            voronoi_zipcode_intersection_proportions,
            postcodes=[1, 2, 3],
            tau=1,
            self_loops=True,
        )
        .with_columns(time=((pl.col("time") - pl.lit(base_time)) / us).cast(pl.Int64))
        .sort(["origin", "dest", "time", "count"])
    )
    assert true_flows_k_0.join(
        flows_k_0, on=true_flows_k_0.columns, how="anti"
    ).is_empty()

    # check self_loops
    flows_k_0 = (
        trajectory.build_zipcode_flows(
            v_flows_k_0,
            v_stayers_k_0,
            voronoi_zipcode_intersection_proportions,
            postcodes=[1, 2, 3],
            tau=1,
            self_loops=False,
        )
        .with_columns(time=((pl.col("time") - pl.lit(base_time)) / us).cast(pl.Int64))
        .sort(["origin", "dest", "time", "count"])
    )
    assert (
        true_flows_k_0.filter(pl.col("origin") != pl.col("dest"))
        .join(
            flows_k_0,
            on=true_flows_k_0.columns,
            how="anti",
        )
        .is_empty()
    )

    # set order of neighborhood k to 1
    trajectory.set_neighborhoods(trajectory.build_neighborhoods(TESSELLATION, k=1))
    v_flows_k_1, v_stayers_k_1 = trajectory.build_cell_flows(tau=1, w=2)
    flows_k_1 = (
        trajectory.build_zipcode_flows(
            v_flows_k_1,
            v_stayers_k_1,
            voronoi_zipcode_intersection_proportions,
            postcodes=[1, 2, 3],
            tau=1,
            self_loops=True,
        )
        .with_columns(time=((pl.col("time") - pl.lit(base_time)) / us).cast(pl.Int64))
        .sort(["origin", "dest", "time", "count"])
    )
    assert true_flows_k_1.join(
        flows_k_1, on=true_flows_k_1.columns, how="anti"
    ).is_empty()


def test_cell_trajectory_constructor():
    with pytest.raises(TypeError) as type_err:
        CellTrajectory(TDF, v_id_col="vid")
    assert (
        "Cell trajectory dataframe does not contain cell IDs or cell IDs column does not match what was set."
        in str(type_err.value)
    )

    with pytest.raises(TypeError) as type_err:
        CellTrajectory(TDF, time_col="time")
    assert (
        "Cell trajectory dataframe does not contain a time column or time column does not match what was set."
        in str(type_err.value)
    )

    with pytest.raises(TypeError) as type_err:
        CellTrajectory(TDF, uid_col="bla")
    assert (
        "Cell trajectory dataframe does not contain a uid column or uid column does not match what was set."
        in str(type_err.value)
    )


def test_mapping_with_invalid_tessellation():
    with pytest.raises(TypeError) as type_err:
        traj = Trajectory(TDF, v_id_col="vid")
        traj.mapping(TESSELLATION)
    assert (
        "Cell trajectory dataframe does not contain cell IDs or cell IDs column does not match what was set."
        in str(type_err.value)
    )


def test_trajectory_constructor():
    with pytest.raises(TypeError) as type_err:
        Trajectory(TDF, longitude="lan")
    assert (
        "Cell trajectory dataframe does not contain a longitude column or the longitude column does not match what was set."
        in str(type_err.value)
    )

    with pytest.raises(TypeError) as type_err:
        Trajectory(TDF, latitude="lan")
    assert (
        "Cell trajectory dataframe does not contain a latitude column or the latitude column does not match what was set."
        in str(type_err.value)
    )

    with pytest.raises(TypeError) as type_err:
        Trajectory(TDF, time_col="time")
    assert (
        "Cell trajectory dataframe does not contain a time column or time column does not match what was set."
        in str(type_err.value)
    )

    with pytest.raises(TypeError) as type_err:
        Trajectory(TDF, uid_col="bla")
    assert (
        "Cell trajectory dataframe does not contain a uid column or uid column does not match what was set."
        in str(type_err.value)
    )
