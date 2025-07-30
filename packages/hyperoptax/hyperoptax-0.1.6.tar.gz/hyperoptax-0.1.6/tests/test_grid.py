import jax.numpy as jnp
import pytest

from hyperoptax.grid import GridSearch
from hyperoptax.spaces import LinearSpace


class TestGridSearch:
    def setup_method(self):
        self.domain_1d = {"x": LinearSpace(-1, 1, 101)}
        self.f_1d = lambda x: -(x**2) + 10
        self.domain_2d = self.domain_1d | {"y": LinearSpace(-2, 2, 101)}
        self.f_2d = lambda x, y: -(x**2 + y**2) + 10

    def test_1d_grid_search(self):
        grid_search = GridSearch(self.domain_1d, self.f_1d)
        result = grid_search.optimize(n_iterations=-1, n_vmap=1)
        assert jnp.allclose(result, jnp.array([0]))

    def test_2d_grid_search(self):
        grid_search = GridSearch(self.domain_2d, self.f_2d)
        result = grid_search.optimize(n_iterations=-1, n_vmap=1)
        assert jnp.allclose(result, jnp.array([0, 0]))

    def test_mismatched_domain_and_function(self):
        with pytest.raises(AssertionError):
            GridSearch(self.domain_1d, self.f_2d)

    def test_n_parallel_10(self):
        grid_search = GridSearch(self.domain_1d, self.f_1d)
        result = grid_search.optimize(n_vmap=10)
        assert jnp.allclose(result, jnp.array([0]))

    def test_jit(self):
        grid_search = GridSearch(self.domain_1d, self.f_1d)
        result = grid_search.optimize(n_iterations=1000, n_vmap=10, jit=True)
        assert jnp.allclose(result, jnp.array([0]))

    def test_n_iterations_not_multiple_of_parallel(self):
        grid_search = GridSearch(self.domain_1d, self.f_1d)
        result = grid_search.optimize(n_iterations=100, n_vmap=7)
        assert jnp.allclose(result, jnp.array([0]))

    def test_domain_is_shuffled_when_random_search(self):
        random_search = GridSearch(self.domain_1d, self.f_1d, random_search=True)
        assert random_search.domain.shape[0] == len(self.domain_1d["x"])
        assert not jnp.allclose(random_search.domain, self.domain_1d["x"].array)

    def test_pmap_grid_search(self):
        grid_search = GridSearch(self.domain_2d, self.f_2d)
        result = grid_search.optimize(n_iterations=10000, n_vmap=4, n_pmap=4)
        assert jnp.allclose(result, jnp.array([0, 0]))

    def test_sharded_grid_search_with_too_many_shards(self):
        grid_search = GridSearch(self.domain_2d, self.f_2d)
        with pytest.raises(AssertionError):
            grid_search.optimize(n_iterations=100, n_vmap=4, n_pmap=5)
