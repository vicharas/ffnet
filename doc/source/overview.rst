--------
Overview
--------

**ffnet is a fast and easy-to-use feed-forward neural network training solution for python.**

*Unique features*:
    1. Any network connectivity without cycles is allowed.
    2. Training can be performed with use of several optimization schemes including: standard backpropagation with momentum, rprop, conjugate gradient, bfgs, tnc (with multiprocessing), genetic alorithm based optimization.
    3. There is access to exact partial derivatives of network outputs vs. its inputs.
    4. Automatic normalization of data.

*Basic assumptions and limitations*:
    1. Network has feed-forward architecture.
    2. Input units have identity activation function, all other units have sigmoid activation function.
    3. Provided data are automatically normalized, both input and output, with a linear mapping to the range (0.15, 0.85). Each input and output is treated separately (i.e. linear map is unique for each input and output).
    4. Function minimized during training is a sum of squared errors of each output for each training pattern.

*Performance*:
    Excellent computational performance is achieved implementing core functions in fortran 77 and wrapping them with f2py. ffnet outstands in performance pure python training packages and is competitive to 'compiled language' software. Incorporation of multiprocessing capabilities (tnc algorithm so far) makes ffnet ideal for large scale (really!) problems. Moreover, a trained network can be exported to fortran sources, compiled and called from many programming languages.

*Usage*:
    Basic usage of the library is outlined below::

        from ffnet import ffnet, mlgraph, savenet, loadnet, exportnet
        conec = mlgraph( (2,2,1) )
        net = ffnet(conec)
        input = [ [0.,0.], [0.,1.], [1.,0.], [1.,1.] ]
        target  = [ [1.], [0.], [0.], [1.] ]
        net.train_tnc(input, target, maxfun = 1000)
        net.test(input, target, iprint = 2)
        savenet(net, "xor.net")
        exportnet(net, "xor.f")
        net = loadnet("xor.net")
        answer = net( [ 0., 0. ] )
        partial_derivatives = net.derivative( [ 0., 0. ] )

    Read API :ref:`documentation <apidoc>` and :ref:`examples <examples>` for more info.

*Graphical user interface*
    As of version 0.8.3 ffnet has GUI called **ffnetui**. ffnetui is a separate project and it is not guaranteed, that the functionalities of both will be kept indentical.