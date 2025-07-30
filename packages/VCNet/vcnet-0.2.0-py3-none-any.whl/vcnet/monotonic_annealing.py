"""Monotonic Annealing callback module"""

from lightning.pytorch.callbacks import Callback


class MonotonicAnnealing(Callback):
    """Monotonic annealing strategy [Bowman et al, 2016] is to start with loss weight equals to 0
         and gradually increase its value over each epoch during training.
         In the case of VCNet, we update the `lambda_KLD` hyperparameter. It is increased by a step
         value of `k_step` for each epoch until it reaches a maximum value `k_max`.

    S. Bowman, L. Vilnis, O. Vinyals, A. Dai, R. Jozefowicz, and S. Bengio. Generating sentences
    from a continuous space. In Proceedings of the 20th SIGNLL Conference on Computational Natural
    Language Learning, pages 10–21, 2016.

    Example
    --------

    This callback can be used while defining the Lightning Trainer, for instance:
    ```
    trainer = L.Trainer(..., callbacks=[ MonotonicAnnealing(0.2,1) ], ...)
    ```

    Warning
    --------
    Using this callback will change any predefined values of the hyperparameter `lambda_KLD`
    """

    def __init__(self, k_step, k_max, *args, **kwargs):
        """Monotonic Annealing callback

        Args:
            k_step (float): value of a step to increase the hyper-parameter. Must be strictly
            positive.
            k_max (float): maximum value of the hyperparameter
        """
        super().__init__(*args, **kwargs)
        assert k_step > 0 and k_max >= k_step
        self.k_step = k_step
        self.k_max = k_max

    def on_train_start(self, trainer, vcnet_module):
        print("MonotonicAnnealing is activated!")
        vcnet_module.lambda_KLD = 0

    def on_train_epoch_start(self, trainer, vcnet_module):
        try:
            if vcnet_module.lambda_KLD < self.k_max:
                vcnet_module.lambda_KLD += self.k_step
                vcnet_module.lambda_KLD = min(vcnet_module.lambda_KLD, self.k_max)
        except:
            print(
                "Error in updating the hyper-parameter `lambda_KLD`: are you sure to use model\
                   that inherits from  VCNetBase?"
            )
