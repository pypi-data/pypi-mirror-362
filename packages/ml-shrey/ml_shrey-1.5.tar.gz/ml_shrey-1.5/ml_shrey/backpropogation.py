import math

def sigmoid(x):
    return 1 / (1 + math.exp(-x))

def train_xor(iterations=1000):
    x1 = [0, 0, 1, 1]
    x2 = [0, 1, 0, 1]
    t = [0, 1, 1, 0]

    # Initial weights and biases
    b1, w11, w21 = -0.3, 0.21, 0.15
    b2, w12, w22 = 0.25, -0.4, 0.1
    b3, w13, w23 = -0.4, -0.2, 0.3

    print("Initial Weights:")
    print("w11: %.2f, w12: %.2f, w21: %.2f, w22: %.2f, w13: %.2f, w23: %.2f\n" %
          (w11, w12, w21, w22, w13, w23))

    iteration = 0
    while iteration < iterations:
        for i in range(4):
            # Forward pass
            z_in1 = b1 + x1[i] * w11 + x2[i] * w21
            z_in2 = b2 + x1[i] * w12 + x2[i] * w22

            z1 = round(sigmoid(z_in1), 4)
            z2 = round(sigmoid(z_in2), 4)

            y_in = b3 + z1 * w13 + z2 * w23
            y = round(sigmoid(y_in), 4)

            # Backpropagation
            del_k = round((t[i] - y) * y * (1 - y), 4)

            w13 = round(w13 + del_k * z1, 4)
            w23 = round(w23 + del_k * z2, 4)
            b3 = round(b3 + del_k, 4)

            del_1 = del_k * w13 * z1 * (1 - z1)
            del_2 = del_k * w23 * z2 * (1 - z2)

            b1 = round(b1 + del_1, 4)
            w11 = round(w11 + del_1 * x1[i], 4)
            w12 = round(w12 + del_1 * x1[i], 4)

            b2 = round(b2 + del_2, 4)
            w21 = round(w21 + del_2 * x2[i], 4)
            w22 = round(w22 + del_2 * x2[i], 4)

            print("Iteration:", iteration)
            print("w11: %.4f, w12: %.4f, w21: %.4f, w22: %.4f, w13: %.4f, w23: %.4f" %
                  (w11, w12, w21, w22, w13, w23))
            print("Error: %.4f\n" % del_k)

            iteration += 1
            if iteration >= iterations:
                break

def backpropagation(*args, **kwargs):
    return train_xor(*args, **kwargs)
