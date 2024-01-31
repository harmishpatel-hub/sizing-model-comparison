def depth_range(x):
    if x < 10:
        return 10
    elif x > 80:
        return 80
    else:
        return round(x)

def post_processing(df, data, model_used, predictions):
    df['Shape'] = data['Shape']
    df['Actual Depth'] = data['Actual Depth']
    df[f"{model_used} Depth"] = predictions
    df[f"{model_used} Depth"] = df[f"{model_used} Depth"].apply(lambda x: depth_range(x))
    df['Depth Difference'] = abs(df['Actual Depth'] - df[f"{model_used} Depth"])
    return df
