# Standard Libraries
import tempfile

# External Libraries
import ray
import pytest
import pandas as pd
import deltalake as dl

# Internal Libraries
import deltaray


@pytest.fixture(scope='session')
def ray_cluster():
    # Start the Ray Cluster
    ray.init(num_cpus=1)

    # Yield control back to test
    yield

    # Stop Ray cluster
    ray.shutdown()


def test_import():
    from deltaray import read_delta


def test_ray_cluster(ray_cluster):
    @ray.remote
    def identity(x):
        return x

    result = ray.get(identity.remote(42))
    assert result == 42


def test_read_deltatable(ray_cluster):
    with tempfile.TemporaryDirectory() as tmp:
        table_uri = f'{tmp}/delta-table'
        df = pd.DataFrame({'id': [0, 1, 2, ], })
        dl.write_deltalake(table_uri, df)

        ds = deltaray.read_delta(table_uri)
        df_read = ds.to_pandas()

    assert df.equals(df_read)
