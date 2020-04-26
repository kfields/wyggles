class WyggleBrain(Brain):
    def __init__(self, model):
        super().__init__(model)
        with root() as root:
            with sensor(See):
            with selector():
                with clause(_I, _see_food) as sees:                
                    with action() as a:
                        async def fn(task, msg):
                            while True:
                                self.move_to(sees.position)
                                self.sleep()
                        a.use(fn)
                with action() as a:
                    async def fn(task, msg):
                        print('b count: ', q.count)
                    a.use(fn)

        self.schedule(root)
