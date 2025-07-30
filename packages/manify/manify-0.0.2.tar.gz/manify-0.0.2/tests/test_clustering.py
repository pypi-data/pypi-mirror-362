import torch

from manify.clustering import RiemannianFuzzyKMeans
from manify.manifolds import ProductManifold


def test_riemannian_fuzzy_k_means():
    pm = ProductManifold(signature=[(-1.0, 4), (-1.0, 2), (0.0, 2), (1.0, 2), (1.0, 4)])
    X, _ = pm.gaussian_mixture(num_points=100)

    for optimizer in ["adam", "adan"]:
        kmeans = RiemannianFuzzyKMeans(pm=pm, n_clusters=5, random_state=42)
        kmeans.fit(X)
        preds = kmeans.predict(X)
        assert preds.shape == (100,), f"Predictions should have shape (100,) (optimizer: {optimizer})"

        # Also test with X as a numpy array
        X_np = X.numpy()
        kmeans = RiemannianFuzzyKMeans(pm=pm, n_clusters=5, random_state=42)
        kmeans.fit(X_np)
        preds_np = kmeans.predict(X_np)
        assert torch.tensor(preds_np).shape == (100,), f"Predictions should have shape (100,) (optimizer: {optimizer})"
        assert torch.allclose(torch.tensor(preds_np), torch.tensor(preds)), (
            "Predictions should be the same for numpy and torch inputs"
        )

        # Also do a single manifold
        kmeans = RiemannianFuzzyKMeans(pm=pm.P[0], n_clusters=5, optimizer=optimizer, random_state=42)
        X0 = pm.factorize(X)[0]
        kmeans.fit(X0)
        preds = kmeans.predict(X0)
        assert preds.shape == (100,), f"Predictions should have shape (100,) (optimizer: {optimizer})"
