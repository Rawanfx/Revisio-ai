from db.vector_store import client
from qdrant_client.models import Filter, FieldCondition, MatchValue

COLLECTION_NAME ="lecture_chunks" 

def retrivie_lecture_grouped(lecture_id : str , question_count : int)->list[dict]:
    all_chunks,_ = client.scroll(
        collection_name=COLLECTION_NAME,
        scroll_filter=Filter(
            must =[FieldCondition(key ="lecture_id",match = MatchValue(value=lecture_id))]
        ),
        with_payload=True,
        limit = 1000
    )
    if not all_chunks:
        return []
    stored_chunks = sorted (all_chunks,key = lambda p:p.payload["chunk_index"])
    groups = split_into_groups(stored_chunks,200)
    question_per_group=distribute_question (question_count,len (groups))
    return [
        {
            "content": "\n\n".join(c.payload["content"] for c in group),
            "questions_count": q_count
        }
        for group, q_count in zip(groups, question_per_group)
    ]


def distribute_question (total_question :int,num_groups:int)->list[int]:
    base = total_question//num_groups
    reminder = total_question%num_groups
    result =[]
    for i in range (num_groups): 
        if i<reminder :
            result.append (base+1)
        else :
            result.append (base)    
    return result        


def split_into_groups (chunks :list,group_size :int=200)->list[list]:
    groups =[]
    i=0
    while (i<len(chunks)):
        group = chunks[i:i+group_size]
        groups.append(group)
        i+=group_size
    return groups    
