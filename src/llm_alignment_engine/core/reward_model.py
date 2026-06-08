import torch
import torch.nn as nn
from transformers import PreTrainedModel, PreTrainedTokenizer

class ProximalRewardModel(nn.Module):
    """
    Reward model utilizing proximal policy mechanics to evaluate text safety
    and mitigate prompt vulnerabilities.
    Designed to shrink checkpoint convergence cycles while restricting untrusted inference.
    """
    def __init__(self, base_model: PreTrainedModel, tokenizer: PreTrainedTokenizer, config):
        super().__init__()
        self.base_model = base_model
        self.tokenizer = tokenizer
        self.hidden_size = config.hidden_size
        
        # Head for computing the scalar reward
        self.value_head = nn.Linear(self.hidden_size, 1, bias=False)
        self.init_weights()
        
    def init_weights(self):
        nn.init.normal_(self.value_head.weight, mean=0.0, std=0.01)

    def forward(self, input_ids, attention_mask=None, **kwargs):
        """
        Forward pass extracting hidden states and computing scalar safety reward.
        """
        outputs = self.base_model(
            input_ids,
            attention_mask=attention_mask,
            output_hidden_states=True,
            **kwargs
        )
        
        # Typically use the last hidden state of the last token (EOS token)
        last_hidden_states = outputs.hidden_states[-1]
        
        # Assuming sequence length, extracting the last token state for each sequence in batch
        batch_size = input_ids.shape[0]
        sequence_lengths = attention_mask.sum(dim=-1) - 1
        
        pooled_states = last_hidden_states[torch.arange(batch_size, device=last_hidden_states.device), sequence_lengths]
        
        # Compute scalar reward
        rewards = self.value_head(pooled_states)
        
        return rewards

    def compute_proximal_loss(self, old_logprobs, new_logprobs, rewards, advantages, clip_ratio=0.2):
        """
        Calculates PPO-style clipped loss for robust optimization.
        """
        ratio = torch.exp(new_logprobs - old_logprobs)
        surr1 = ratio * advantages
        surr2 = torch.clamp(ratio, 1.0 - clip_ratio, 1.0 + clip_ratio) * advantages
        
        loss = -torch.min(surr1, surr2).mean() - rewards.mean() * 0.01 # Adding small reward bonus
        return loss

if __name__ == "__main__":
    print("Proximal Reward Model Initialized for Alignment Evaluation.")
