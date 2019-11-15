import numpy as np
import pandas as pd





def append_cumsum(data_frame, count_col=None, survive_mode=False):
    df = data_frame.copy()
    count_sum = df[count_col].sum()
    cumsum_col = '{}_cumsum'.format(count_col)
    cumsum_ratio_col = '{}_cumsum_ratio'.format(count_col)
    df[cumsum_col] = df[count_col].cumsum()
    df[cumsum_ratio_col] = df[cumsum_col] / count_sum

    if survive_mode:
        cumsum_shifted_col = '{}_shifted'.format(cumsum_col)
        surviving_col = '{}_suviving'.format(count_col)
        surviving_ratio_col = '{}_suviving_ratio'.format(count_col)
        temp_columns = [cumsum_col, cumsum_ratio_col, cumsum_shifted_col]
        df[cumsum_shifted_col] = df[cumsum_col].shift(1)
        df[cumsum_shifted_col].fillna(0, inplace=True)
        df[surviving_col] = df[cumsum_shifted_col].apply(lambda x: count_sum - x)
        df[surviving_ratio_col] = df[surviving_col] / count_sum
        df.drop(temp_columns, axis=1, inplace=True)
    return df


def count_value(data_frame, value_col='', with_ratio=True, sort_index=True, fill_index=True, cum_ratio=True,
                survive_mode=True):
    df = data_frame.copy()
    df_count_value = df[value_col].value_counts()
    if sort_index:
        df_count_value = df_count_value.sort_index()
        if fill_index:
            step = np.min(np.diff(df_count_value.index.values))
            start = np.min(df_count_value.index.values)
            stop = np.max(df_count_value.index.values) + 1
            df_count_value = df_count_value.reindex(pd.RangeIndex(start=start, stop=stop, step=step), fill_value=0)
    df_count_value = df_count_value.reset_index()
    count_col = '{}_count'.format(value_col)
    ratio_col = '{}_ratio'.format(value_col)
    df_count_value.columns = [value_col, count_col]

    if with_ratio:
        count_sum = sum(df_count_value[count_col])
        df_count_value[ratio_col] = df_count_value[count_col] / count_sum

    if cum_ratio:
        df_count_value = append_cumsum(df_count_value, count_col=count_col, survive_mode=survive_mode)

    return df_count_value


def append_group_cumsum(data_frame, count_col=None, group_cols=None, survive_mode=False):
    df = data_frame.copy()
    count_sum = df.groupby(group_cols)[count_col].sum()
    cumsum_col = '{}_cumsum'.format(count_col)
    cumsum_ratio_col = '{}_cumsum_ratio'.format(count_col)
    df[cumsum_col] = df.groupby(group_cols)[count_col].cumsum()
    df[cumsum_ratio_col] = df.groupby(group_cols)[cumsum_col] / count_sum

    if survive_mode:
        cumsum_shifted_col = '{}_shifted'.format(cumsum_col)
        surviving_col = '{}_suviving'.format(count_col)
        surviving_ratio_col = '{}_suviving_ratio'.format(count_col)
        temp_columns = [cumsum_col, cumsum_ratio_col, cumsum_shifted_col]
        df[cumsum_shifted_col] = df[cumsum_col].shift(1)
        df[cumsum_shifted_col].fillna(0, inplace=True)
        df[surviving_col] = df[cumsum_shifted_col].apply(lambda x: count_sum - x)
        df[surviving_ratio_col] = df[surviving_col] / count_sum
        df.drop(temp_columns, axis=1, inplace=True)
    return df


def count_value_by_group(data_frame, value_col='', group_cols=None, with_ratio=True, sort_index=True, fill_index=False,
                         cum_ratio=True,
                         survive_mode=True):
    df = data_frame.copy()
    df['dummy_col'] = 1
    count_cols = list()
    count_cols.extend(group_cols)
    count_cols.append(value_col)

    df_count_value = df.groupby(count_cols)['dummy_col'].count()

    if sort_index:
        df_count_value = df_count_value.sort_index()

        if fill_index:
            enum_index = df_count_value.index.levels[:-1]
            enum_index = [list(x) for x in enum_index]
            value_index = df_count_value.index.levels[-1].tolist()
            step = np.min(np.diff(value_index))
            start = np.min(value_index)
            stop = np.max(value_index) + step
            value_range_index = list(range(start, stop, step))
            enum_index.append(value_range_index)
            df_count_value = df_count_value.reindex(itertools.product(*enum_index), fill_value=0)

    df_count_value = df_count_value.reset_index()
    count_col = "{value_col}_count".format(value_col=value_col)
    cols = count_cols.copy()
    cols.append(count_col)
    df_count_value.columns = cols

    count_col = '{}_count'.format(value_col)
    ratio_col = '{}_ratio'.format(value_col)

    if with_ratio:
        count_sum = df_count_value.groupby(group_cols)[count_col].sum().reset_index().rename(
            columns={count_col: 'count_sum'})
        df_count_value = df_count_value.merge(count_sum, on=group_cols)
        df_count_value[ratio_col] = df_count_value[count_col] / df_count_value['count_sum']

    if cum_ratio:
        # df_count_value = append_cumsum(df_count_value, count_col=count_col, survive_mode=survive_mode)
        cumsum_col = '{}_cumsum'.format(count_col)
        cumsum_ratio_col = '{}_cumsum_ratio'.format(count_col)
        df_count_value[cumsum_col] = df_count_value.groupby(group_cols)[count_col].cumsum()
        df_count_value[cumsum_ratio_col] = df_count_value.groupby(group_cols)[ratio_col].cumsum()
        if survive_mode:
            cumsum_shifted_col = '{}_shifted'.format(cumsum_col)
            surviving_col = '{}_suviving'.format(count_col)
            surviving_ratio_col = '{}_suviving_ratio'.format(count_col)
            temp_columns = [cumsum_col, cumsum_ratio_col, cumsum_shifted_col]
            df_count_value[cumsum_shifted_col] = df_count_value[cumsum_col].shift(1)
            df_count_value[cumsum_shifted_col].fillna(0, inplace=True)
            df_count_value[surviving_col] = df_count_value['count_sum'] - df_count_value[cumsum_shifted_col]
            df_count_value[surviving_ratio_col] = df_count_value[surviving_col] / df_count_value['count_sum']
            df_count_value.drop(temp_columns, axis=1, inplace=True)

    return df_count_value