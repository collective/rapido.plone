def create_external_record(context):
    other = context.rapido('otherapp')
    record = other.create_record()
    record['something'] = 12
    return len(other.records())
