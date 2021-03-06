from flask import current_app

def add_to_index(index, model):
    if not current_app.elasticsearch:
        return
    payload = {}
    for field in model.__searchable__:
        payload[field] = getattr(model, field)
    current_app.elasticsearch.index(index=index, id=model.id,
                                    document=payload)

def remove_from_index(index, model):
    if not current_app.elasticsearch:
        return
    current_app.elasticsearch.delete(index=index, id=model.id)

def query_index(index, search, page, per_page, min_score, fields):
    if not current_app.elasticsearch:
        return [], 0, 0
    search = current_app.elasticsearch.search(
        index=index,
        body={'query': {'combined_fields': {'query': search, 'fields': fields, "operator": "and"}}, #make this into a variable
            'from': (page - 1) * per_page, 'size': per_page, 
            "min_score": min_score})
    ids = [int(hit['_id']) for hit in search['hits']['hits']]
    return ids, search['hits']['total']['value'], search['hits']['max_score']

