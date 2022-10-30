import falcon

class Health:
    async def on_get(self, req: falcon.Request, resp: falcon.Response):
        resp.text = 'healthy'
        resp.status = falcon.HTTP_200
