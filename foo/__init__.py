import dock


@dock
def package_function():
    ...


@dock
class PackageClass:
    
    @dock
    def __init__(self):
        ...
    
    @dock
    def asdf(self):
        ...

    @dock
    class InnerPackageClass:
        @dock
        def __init__(self):
            ...
        
        @dock
        def asdf(self):
            ...
