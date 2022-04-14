class ScanningContextStrategy:
    strategy = None

    def setStrategy(self, strategy):
        self.strategy = strategy

    async def executeStrategy(self):
        return await self.strategy.execute()
