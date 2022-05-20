trained_model = Net()
trained_model.load_state_dict(torch.load('SINet/snapshot/SINet_V2/Net_epoch_best.pth'))

# Export the trained model to ONNX
dummy_input = Variable(torch.randn(1, 1, 256, 256)) # one black and white 28 x 28 picture will be the input to the model
torch.onnx.export(trained_model, dummy_input, "output/mnist.onnx")