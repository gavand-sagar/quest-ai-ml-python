# # ============================================
# # SAVING & LOADING MODELS IN PYTORCH
# # Goal: Train a tiny XOR model ONCE, then save it 3 ways
# #       and load it back, so you never have to retrain.
# #
# # We cover the THREE saving styles you will actually meet:
# #   1) state_dict   -> the RECOMMENDED PyTorch way (weights only)
# #   2) whole model  -> the QUICK way (pickles the whole object)
# #   3) ONNX export  -> the PORTABLE way (run it from C#, Java, JS...)
# #
# # The same trained model is reused for all three so you can see
# # that they produce the SAME predictions.
# # ============================================

import torch
import torch.nn as nn
import torch.optim as optim

# We keep the model definition in a function so BOTH training and
# loading (method 1) can build the exact same architecture.
def build_model():
    # 2 inputs -> hidden(8) -> ReLU -> 1 output.
    # NOTE: the final layer outputs a RAW LOGIT (no Sigmoid here).
    # The C# consumer applies sigmoid itself, so we keep the graph
    # simple and let the caller decide the activation.
    return nn.Sequential(
        nn.Linear(2, 8),
        nn.ReLU(),
        nn.Linear(8, 1),
    )


# ============================================
# STEP 1: DATA + TRAIN (the XOR problem)
# ============================================
X = torch.tensor([[0.0, 0.0],
                  [0.0, 1.0],
                  [1.0, 0.0],
                  [1.0, 1.0]])
y = torch.tensor([[0.0], [1.0], [1.0], [0.0]])

torch.manual_seed(1)                 # repeatable results
model = build_model()

# BCEWithLogitsLoss expects RAW LOGITS (matches our no-sigmoid model).
loss_fn = nn.BCEWithLogitsLoss()
optimizer = optim.Adam(model.parameters(), lr=0.1)

for epoch in range(3000):
    y_pred = model(X)
    loss = loss_fn(y_pred, y)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

print(f"Trained. Final loss = {loss.item():.4f}\n")


def predict(m):
    # eval() + no_grad() is how you should ALWAYS run inference:
    #   - eval() turns off dropout / batchnorm training behaviour
    #   - no_grad() skips gradient tracking (faster, less memory)
    m.eval()
    with torch.no_grad():
        logits = m(X)
        probs = torch.sigmoid(logits)   # turn logits into 0..1 probabilities
    for i in range(4):
        print(f"   {X[i].tolist()} -> {probs[i].item():.2f}")


print("Original model predictions:")
predict(model)
print()


# ============================================
# METHOD 1: state_dict  (RECOMMENDED)
# ============================================
# A state_dict is just a Python dict of {layer_name: weight_tensor}.
# You save ONLY the numbers, not the code. To load, you must first
# re-create the SAME architecture, then pour the weights back in.
#
# WHY this is the best practice:
#   - Small file, no pickled source code.
#   - Not tied to your file/class layout, so refactors don't break it.
#   - Safe(r) to load: it doesn't execute arbitrary objects.
SD_PATH = "xor_state_dict.pth"
torch.save(model.state_dict(), SD_PATH)     # <- save weights only

# --- load it back ---
loaded_sd = build_model()                   # 1) rebuild same architecture
dict_data = torch.load(SD_PATH, weights_only=True)
loaded_sd.load_state_dict(dict_data)  # 2) load weights
# weights_only=True (PyTorch 2.x) avoids un-pickling arbitrary code = safer.

print("[Method 1] Loaded from state_dict:")
predict(loaded_sd)
print()


# ============================================
# METHOD 2: whole model  (QUICK, but fragile)
# ============================================
# torch.save(model) pickles the ENTIRE object graph. On load you get
# the model back WITHOUT redefining the class... as long as the exact
# same code is importable in the loading environment.
#
# DOWNSIDES (why teams avoid this for anything long-lived):
#   - Brittle: rename the file/class and loading breaks.
#   - Unsafe: unpickling runs code -> never load untrusted .pth files.
#   - Ties the checkpoint to your project structure.
FULL_PATH = "xor_full_model.pth"
torch.save(model, FULL_PATH)                # <- save the whole object

# For a self-authored file we trust, allow the full (non weights_only) load.
loaded_full = torch.load(FULL_PATH, weights_only=False)

print("[Method 2] Loaded whole model:")
predict(loaded_full)
print()


# ============================================
# METHOD 3: ONNX export  (PORTABLE / cross-language)
# ============================================
# ONNX is a framework-neutral format. Export once here, then run it
# from C#, Java, JavaScript, etc. via ONNX Runtime -- no Python needed.
#
# KEY EXPORT DETAILS THAT MATTER TO THE CONSUMER (e.g. our C# app):
#   - input_names / output_names: the C# code looks these up BY NAME.
#     We name the input "input" so the C# NamedOnnxValue matches.
#   - dynamic_axes: mark the batch dimension as variable so the same
#     model accepts 1 row or 100 rows without re-exporting.
#   - Always export in eval() mode with a representative dummy input.
ONNX_PATH = "xor_model.onnx"
model.eval()
dummy_input = torch.zeros(1, 2)             # shape [batch=1, features=2]

torch.onnx.export(
    model,
    dummy_input,
    ONNX_PATH,
    input_names=["input"],                  # <- must match the C# consumer
    output_names=["output"],
    dynamic_axes={"input": {0: "batch"},     # row count can vary at runtime
                  "output": {0: "batch"}},
    opset_version=17,                       # pin the opset for reproducibility
    dynamo=False,                           # use the stable, well-supported exporter
)
print(f"[Method 3] Exported ONNX -> {ONNX_PATH}")
print("   Consume it from C# with Microsoft.ML.OnnxRuntime (see Program.cs).\n")


# ============================================
# DOs and DON'Ts WHEN SAVING MODELS
# ============================================
# DO:
#   - Prefer state_dict for PyTorch-to-PyTorch checkpoints.
#   - Save the architecture code alongside the weights (in git).
#   - Save extra training state for RESUMING: also store optimizer
#     state_dict, epoch, and loss in one dict, e.g.:
#         torch.save({"model": model.state_dict(),
#                     "opt": optimizer.state_dict(),
#                     "epoch": epoch}, "ckpt.pth")
#   - Call model.eval() before inference/export.
#   - Pin versions (torch, opset) so results are reproducible.
#   - Use weights_only=True when loading checkpoints you didn't create.
#   - Use ONNX (or TorchScript) for deployment to other languages/runtimes.
#
# DON'T:
#   - Don't load whole-model .pth files from untrusted sources (code exec).
#   - Don't rely on method 2 across refactors -- moving the class breaks it.
#   - Don't forget input/output NAMES when exporting ONNX -- consumers need them.
#   - Don't hard-code a fixed batch size in ONNX if inputs will vary.
#   - Don't commit huge weight files to git without Git LFS.
print("Done. Files written:",
      SD_PATH, "|", FULL_PATH, "|", ONNX_PATH)
