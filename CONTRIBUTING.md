# Contributing

## Issues

Issues are very valuable to this project.

* Ideas are a valuable source of contributions others can make
* Problems show where this project is lacking
* With a question you show where contributors can improve the user experience

## Pull Requests

Pull requests are, a great way to get your ideas into this repository.

### How to add a `Rule`

The new rule needs to inherit from `AstroidRule`.

Once the class is created, you need to make it visible in the `__init__.py` file.

After that you might want to add it either in `AlwaysApplyPhase` or via an `Optimizer`

### How to add an `Optimizer`

The new optimizer needs to inherit from `Optimizer`, it needs to implement method `visit_[ClassName]` to apply something on this node.

For instance, if you need to count the number of times a method is called, you need to implement the method `visit_Call`. Such as in [RenameOptimizer](pygolf/optimizers/rename_method_optimizer.py)

### Tests

To test you can simply use the target `check` in [Makefile](Makefile), it will reproduce every steps in the [github workflow](.github/workflows/pythonapp.yml) to merge a PR.

## Thanks

Thank you for any contribution you might make :).