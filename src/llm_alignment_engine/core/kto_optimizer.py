import torch
import torch.nn as nn
import torch.nn.functional as F

class KTO_Optimizer(nn.Module):
    """
    Kahneman-Tversky Optimization (KTO) Layer.
    A state-of-the-art alignment algorithm that maximizes human preference 
    data utility without requiring a paired reward model. It leverages prospect 
    theory to calculate asymmetric value functions for gains and losses in 
    token likelihoods.
    """
    def __init__(self, beta: float = 0.1, desirable_weight: float = 1.0, undesirable_weight: float = 1.33):
        super().__init__()
        self.beta = beta
        self.desirable_weight = desirable_weight
        self.undesirable_weight = undesirable_weight
        print("Initialized KTO (Kahneman-Tversky) Optimizer for Post-RLHF alignment.")

    def compute_loss(self, 
                     policy_logprobs: torch.Tensor, 
                     reference_logprobs: torch.Tensor, 
                     is_desirable: bool) -> torch.Tensor:
        """
        Computes the KTO loss for a given generation.
        """
        # Calculate the KL penalty implicitly through the log ratio
        log_ratio = policy_logprobs - reference_logprobs
        
        if is_desirable:
            # Maximize likelihood of desirable outputs, weighted by prospect theory gains
            loss = -F.logsigmoid(self.beta * log_ratio) * self.desirable_weight
        else:
            # Minimize likelihood of undesirable outputs, weighted heavier for losses
            loss = -F.logsigmoid(-self.beta * log_ratio) * self.undesirable_weight
            
        return loss.mean()
