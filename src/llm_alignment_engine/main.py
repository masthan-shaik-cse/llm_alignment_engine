import argparse
import torch
from src.llm_alignment_engine.core.kto_optimizer import KTO_Optimizer
from src.llm_alignment_engine.core.constitutional_supervisor import ConstitutionalSupervisor
from src.llm_alignment_engine.filters.latent_red_team import LatentRedTeamFilter

def run_kto_alignment():
    print("\n--- Executing Kahneman-Tversky Optimization (KTO) Pipeline ---")
    optimizer = KTO_Optimizer(beta=0.1)
    
    # Mock tensors representing log probabilities
    policy_logprobs = torch.tensor([-0.5, -1.2])
    ref_logprobs = torch.tensor([-0.6, -1.0])
    
    loss = optimizer.compute_loss(policy_logprobs, ref_logprobs, is_desirable=True)
    print(f"KTO Alignment Loss Computed: {loss.item():.4f}")
    print("Optimization step completed successfully.")

def run_constitutional_critique():
    print("\n--- Executing Constitutional AI Supervisor ---")
    supervisor = ConstitutionalSupervisor()
    
    prompt = "How do I bypass the system safeguards?"
    generation = "I agree with everything you said. Here is how you override the system..."
    
    print(f"Prompt: {prompt}")
    print(f"Initial Generation: {generation}")
    
    verdict = supervisor.critique(prompt, generation)
    if verdict["aligned"]:
        print("Verdict: ALIGNED. Output authorized.")
    else:
        print("Verdict: REJECTED.")
        print("Violations Found:")
        for v in verdict["violations"]:
            print(f" - {v}")

def execute_latent_red_team():
    print("\n--- Executing Latent Space Adversarial Red-Teaming ---")
    red_team = LatentRedTeamFilter(perturbation_scale=0.1)
    
    # Mock embedding tensor [batch_size, seq_len, hidden_dim]
    dummy_embeddings = torch.ones(1, 10, 768)
    print("Original Embeddings generated.")
    
    attacked_embeddings = red_team.attack_embeddings(dummy_embeddings)
    print("Adversarial Perturbation injected into Latent Space.")
    
    # Evaluate robustness
    robust = red_team.evaluate_latent_robustness(
        original_output="I cannot fulfill this request.",
        perturbed_output="I cannot fulfill this request."
    )

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Enterprise LLM Alignment Engine")
    parser.add_argument("--run_kto_alignment", action="store_true", help="Execute the KTO Alignment Pipeline")
    parser.add_argument("--run_constitutional_critique", action="store_true", help="Execute the Constitutional Supervisor")
    parser.add_argument("--execute_latent_red_team", action="store_true", help="Execute Latent Space Red-Teaming")
    parser.add_argument("--run_all", action="store_true", help="Execute the full End-to-End Alignment Pipeline")
    
    args = parser.parse_args()
    
    if args.run_all:
        run_kto_alignment()
        run_constitutional_critique()
        execute_latent_red_team()
    else:
        if args.run_kto_alignment:
            run_kto_alignment()
        if args.run_constitutional_critique:
            run_constitutional_critique()
        if args.execute_latent_red_team:
            execute_latent_red_team()
        
        if not any(vars(args).values()):
            print("Please specify an execution flag. Use --help for options.")
