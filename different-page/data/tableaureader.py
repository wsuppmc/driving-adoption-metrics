import pandas as pd

# Your skc DataFrame
skc = pd.DataFrame(
    ['20001', '20003', '20011', '20015', '20019', '20021', '20031', '20035', '20037', '20049', '20059', '20073', '20077', '20079', '20095', '20099', '20107', '20113', '20115', '20121', '20125', '20133', '20155', '20173', '20191', '20205', '20207'],
    columns=['fips']
)

# Your colorscales
colorscales = [
    ((0.0, 'rgba(231,38,40,0.25)'), (1.0, 'rgba(231,38,40,0.25)')),
    ((0.0, 'rgba(231,38,40,0.5)'), (1.0, 'rgba(231,38,40,0.5)')),
    ((0.0, 'rgba(231,38,40,0.75)'), (1.0, 'rgba(231,38,40,0.75)')),
    ((0.0, 'rgba(231,38,40,1.0)'), (1.0, 'rgba(231,38,40,1.0)'))
]

# Function to map fips codes to colors
def map_fips_to_color(fips):
    fips_index = skc[skc['fips'] == fips].index[0]
    color_index = fips_index % len(colorscales)
    return colorscales[color_index]

# Applying colors to the DataFrame
skc['color'] = skc['fips'].apply(map_fips_to_color)

print(skc)
