from fastapi import Request, Response, APIRouter

import Repository

router = APIRouter(
    prefix="/api/scheme",
)

@router.get("/{scheme_id}")
async def handle_get(request: Request, scheme_id: int):
    sc_place = request.query_params['sc_place']
    if not bool(sc_place):
        return Response(status_code=400, content='no params to look for')
    data = await Repository.get_data_from_db(sc_place, scheme_id)

    return Response(content=f"the result is: {str(data)} kA", media_type="application/json")


@router.post("")
async def handle_post(request: Request):
    content_type = request.headers['Content-Type']
    if content_type == 'application/xml':
        body = await request.body()
        scheme_id = await Repository.post_data_to_db(body)
        if scheme_id:
            return Response(status_code=200, content=f'completed, scheme {scheme_id} was added',
                            media_type="application/json")
        return Response(status_code=400)


@router.put("/{scheme_id}")
async def handle_put(request: Request, scheme_id: int):
    content_type = request.headers['Content-Type']
    if content_type == 'application/xml':
        body = await request.body()

        completed = await Repository.put_data_to_db(body, scheme_id)

        if completed:
            return Response(status_code=200, content=f'completed, scheme {scheme_id} was patched',
                            media_type="application/json")
        return Response(status_code=400)


@router.delete("/{scheme_id}")
async def handle_deletion(scheme_id: int):
    completed = await Repository.delete_data_from_db(scheme_id)
    if completed:
        return Response(status_code=200, content=f'completed, scheme {scheme_id} was deleted',
                        media_type="application/json")
    return Response(status_code=404)