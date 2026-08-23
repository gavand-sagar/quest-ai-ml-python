using Microsoft.ML.OnnxRuntime;
using Microsoft.ML.OnnxRuntime.Tensors;

// ============================================================
// CONSUMING A PYTORCH-EXPORTED ONNX MODEL FROM C#
// ------------------------------------------------------------
// The model (xor_model.onnx) was trained + exported in Python
// (see Lab21_Save_And_Load_Models.py). ONNX lets us run it here
// with NO Python and NO PyTorch installed -- only ONNX Runtime.
//
// Contract agreed at export time:
//   input  name = "input"   shape [batch, 2]  (two XOR features)
//   output name = "output"  shape [batch, 1]  (a RAW logit)
// The model does NOT apply sigmoid, so we apply it here to turn
// the logit into a 0..1 probability.
// ============================================================

class Program
{
    static void Main(string[] args)
    {
        // BEST PRACTICE: resolve the model path relative to the running
        // app, not a hard-coded absolute path. The .csproj copies the
        // file next to the .exe (CopyToOutputDirectory).
        var modelPath = Path.Combine(AppContext.BaseDirectory, "xor_model.onnx");

        if (!File.Exists(modelPath))
        {
            Console.WriteLine($"Model not found at: {modelPath}");
            return;
        }

        // BEST PRACTICE: create the InferenceSession ONCE and reuse it.
        // It is expensive to build and is thread-safe for Run(). Here a
        // using-block is fine because it is a short-lived console demo.
        using var session = new InferenceSession(modelPath);

        // The four XOR cases -> expected outputs are 0,1,1,0.
        float[][] cases =
        {
            new float[] { 0, 0 },
            new float[] { 0, 1 },
            new float[] { 1, 0 },
            new float[] { 1, 1 },
        };

        Console.WriteLine("XOR predictions from the ONNX model:");

        foreach (var inputData in cases)
        {
            // Build a [1, 2] tensor: batch of 1 row, 2 features.
            var inputTensor = new DenseTensor<float>(inputData, new int[] { 1, 2 });

            var inputs = new List<NamedOnnxValue>
            {
                // The name MUST match the exported input_names=["input"].
                NamedOnnxValue.CreateFromTensor("input", inputTensor)
            };

            using var results = session.Run(inputs);

            var outputTensor = results.First().AsTensor<float>();
            foreach (var logit in outputTensor)
            {
                // Model returns a raw logit -> apply sigmoid to get 0..1.
                var probability = 1.0 / (1.0 + Math.Exp(-logit));
                Console.WriteLine(
                    $"   [{inputData[0]}, {inputData[1]}] -> {Math.Round(probability, 2)}");
            }
        }
    }
}
