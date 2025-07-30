from matplotlib.colors import LinearSegmentedColormap

divergingBlueOrange = LinearSegmentedColormap.from_list('my_CMAP', (
    # Edit this gradient at https://eltos.github.io/gradient/#219EBC-8ECAE6-FFFFFF-FFB703-FB8500
    (0.000, (0.129, 0.620, 0.737)),
    (0.250, (0.557, 0.792, 0.902)),
    (0.500, (1.000, 1.000, 1.000)),
    (0.750, (1.000, 0.718, 0.012)),
    (1.000, (0.984, 0.522, 0.000))))

gradientOrange = LinearSegmentedColormap.from_list('my_gradient', (
    # Edit this gradient at https://eltos.github.io/gradient/#FFCF99-FEB86A-FDA644-FB8500
    (0.000, (1.000, 0.812, 0.600)),
    (0.333, (0.996, 0.722, 0.416)),
    (0.667, (0.992, 0.651, 0.267)),
    (1.000, (0.984, 0.522, 0.000))))

red = '#DB1728'
blue = '#015A8A'

intenseBlueOrange = LinearSegmentedColormap.from_list('progressiveBlueOrange', ['#023047', '#219ebc', '#8ecae6', '#ffb703', '#fb8500']) # Blue orange
intenseGreenOrange = LinearSegmentedColormap.from_list('progressiveGreenOrange', ['#264653', '#2a9d8f', '#e9c46a', '#f4a261', '#e76f51']) # Green orange
gentleBlueOrange = LinearSegmentedColormap.from_list('colourmap', ["#009fb7","#cdd7d6","#dd6e42"])

three_colours = ["#26547c","#ef476f","#ffd166"]

# Colour map from Dr Adrien Houge
HUGE_CMAP_LIST = ['#EDE0D4', '#E6CCB2', '#DDB892', '#B08968', '#9C6644', '#7F5539']
latte = LinearSegmentedColormap.from_list("Cmap", HUGE_CMAP_LIST, N = 200)

phi = (1 + 5 ** 0.5 ) / 2
height = 4.7
width = phi * height
figsize=(width, height)