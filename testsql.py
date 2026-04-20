import pandas as pd

# 1. SETUP: Load your data (Assuming you exported the table to a CSV or a DataFrame)
# df = pd.read_csv('dim_segments.csv') 
# For this example, let's assume 'df' is your bd_warehouse.dim_segments table

def get_all_children(df, starting_id):
    # This list will hold all the children we find
    all_descendants = []
    
    # This is our 'queue' of IDs to look for
    queue = [starting_id]
    
    while len(queue) > 0:
        # Take the first ID out of the queue
        current_parent = queue.pop(0)
        
        # Find all rows where this ID is the parent
        children = df[df['segment_parent_code'] == current_parent]['segment_db_code'].tolist()
        
        # If we found children, add them to our results and the queue
        if children:
            all_descendants.extend(children)
            queue.extend(children)
            
    return all_descendants

# 2. EXECUTE: Find everyone under 349332
starting_parent = 349332
result_ids = get_all_children(df, starting_parent)

print(f"Total children found: {len(result_ids)}")
print(f"List of IDs: {result_ids}")

# sss