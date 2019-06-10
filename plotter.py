import pandas as pd


class Plotter:
    def __init__(self, df):
        self.df = df
        # prepare data
        intervals = [i * 10000000 for i in range(10)]
        intervals.append(float("inf"))
        df['ValueReal'] = df.apply(lambda row: Plotter.value_of_price(row.Value), axis=1)
        df['ValueIntervals'] = pd.cut(df.ValueReal, intervals, include_lowest=True)
        df['WageReal'] = df.apply(lambda row: Plotter.value_of_price(row.Wage), axis=1)
        intervals = [i for i in range(15, 48, 3)]
        df['AgeIntervals'] = pd.cut(df.Age, intervals)

    @staticmethod
    def value_of_price(value):
        length = len(value)
        if length == 2:
            return 0
        letter = value[length - 1]
        value = value[1:length - 1]
        value = float(value)
        if letter == 'M':
            value = value * 1000000
        else:
            value = value * 1000
        return value

    # wykres ceny od overalla
    def overall_and_price_comp(self, ax):
        colors = []
        colors_dict = {}
        grouped = self.df.groupby(['Overall', 'ValueReal']).size()
        number_of_occurrences_df = grouped.to_frame(name='size').reset_index()
        for index, row in number_of_occurrences_df.iterrows():
            colors_dict[str(row['Overall']) + "del" + (str(row['ValueReal']))] = row['size']

        for index, row in self.df[['Overall', 'ValueReal']].iterrows():
            key = str(row['Overall']) + "del" + (str(row['ValueReal']))
            colors.append(colors_dict[key])

        self.df.loc[:, ['Overall', 'ValueReal']] \
            .plot(kind='scatter', x='Overall', y='ValueReal', title='Overall and Price Comparison', ax=ax,
                  c=colors, colormap='plasma')

    # ceny slupkowo
    def price_bar(self, ax):
        self.df['ValueIntervals'].value_counts().sort_index() \
            .plot(kind='bar', title='Footballer Value distribution', ax=ax)

    # cena a pozycja
    def price_position_bar(self, ax):
        title = 'Mean Value for every position'
        self.df.loc[:, ['ValueReal', 'Position']].groupby('Position').mean().plot(kind='bar', title=title, ax=ax)

    # cena a wiek
    def price_age_plot(self, ax):
        title = 'Mean Value for every age interval'
        self.df.loc[:, ['ValueReal', 'AgeIntervals']].groupby('AgeIntervals').mean(). \
            plot(kind='bar', title=title, ax=ax)

    # kluby najbardziej wartościowe
    def most_valued_clubs(self, ax):
        title = 'Most valued clubs'
        self.df.loc[:, ['ValueReal', 'Club']].groupby('Club').sum().sort_values('ValueReal').tail(10) \
            .plot(kind='barh', title=title, ax=ax)

    # rozkład całego zbioru : wiek, pozycja, kraj, zarobki
    def age_distribution(self, ax):
        title = 'Age distribution'
        self.df['AgeIntervals'].value_counts().sort_index().plot(kind='bar', title=title, ax=ax)

    def position_distribution(self, ax):
        title = 'Position distribution'
        self.df['Position'].value_counts().sort_index().plot(kind='pie', title=title, ax=ax)

    def country_distribution(self, ax):
        title = 'Nationality distribution'
        self.df['Nationality'].value_counts().sort_index().plot(kind='bar', title=title, ax=ax)

    # kraje z najlepszymi piłkarzami - mediana
    def best_footballers_by_countries(self, ax):
        title = 'Mean overall by countries'
        self.df.loc[:, ['Overall', 'Nationality']].groupby('Nationality').mean().sort_values('Overall') \
            .plot(kind='barh', title=title, ax=ax)
        for p in ax.patches:
            ax.annotate(str(round(p.get_width(), 1)), xy=(p.get_width() * 1.005, p.get_y() * 1.005))
