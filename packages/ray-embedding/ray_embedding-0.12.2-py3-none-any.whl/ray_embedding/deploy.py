import os

import torch
from ray.serve import Application

from ray_embedding.dto import AppConfig, ModelDeploymentConfig, DeployedModel
from ray_embedding.embedding_model import EmbeddingModel
from ray_embedding.model_router import ModelRouter


def build_model(model_config: ModelDeploymentConfig) -> DeployedModel:
    deployment_name = model_config.deployment
    model = model_config.model
    served_model_name = model_config.served_model_name or os.path.basename(model)
    device = model_config.device
    backend = model_config.backend or "torch"
    matryoshka_dim = model_config.matryoshka_dim
    trust_remote_code = model_config.trust_remote_code or False
    model_kwargs = model_config.model_kwargs or {}

    if "torch_dtype" in model_kwargs:
        torch_dtype = model_kwargs["torch_dtype"].strip()
        if torch_dtype == "float16":
            model_kwargs["torch_dtype"] = torch.float16
        elif torch_dtype == "bfloat16":
            model_kwargs["torch_dtype"] = torch.bfloat16
        elif torch_dtype == "float32":
            model_kwargs["torch_dtype"] = torch.float32
        else:
            raise ValueError(f"Invalid torch_dtype: '{torch_dtype}'")

    deployment = EmbeddingModel.options(name=deployment_name).bind(model=model,
                                                                   served_model_name=served_model_name,
                                                                   device=device,
                                                                   backend=backend,
                                                                   matryoshka_dim=matryoshka_dim,
                                                                   trust_remote_code=trust_remote_code,
                                                                   model_kwargs=model_kwargs
                                                                   )
    return DeployedModel(model=served_model_name,
                         deployment_handle=deployment,
                         batch_size=model_config.batch_size,
                         num_retries=model_config.num_retries
                         )


def build_app(args: AppConfig) -> Application:
    model_router, models = args.model_router, args.models
    assert model_router and models
    assert model_router.path_prefix

    deployed_models = {model_config.served_model_name: build_model(model_config) for model_config in models}
    router = ModelRouter.options(name=model_router.deployment).bind(deployed_models, model_router.path_prefix)
    return router
