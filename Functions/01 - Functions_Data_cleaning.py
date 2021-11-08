{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "f8968566",
   "metadata": {},
   "outputs": [],
   "source": [
    "def clean_dataset(data_model):\n",
    "    assert isinstance(data_model, pd.DataFrame), \"data_model needs to be a pd.DataFrame\"\n",
    "    data_model.dropna(inplace=True)\n",
    "    indices_to_keep = ~data_model.isin([np.nan, np.inf, -np.inf]).any(1)\n",
    "    return data_model[indices_to_keep].astype(np.float64)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "9d864847",
   "metadata": {},
   "outputs": [],
   "source": [
    "def boxcox_transform(data_model):\n",
    "    numeric_cols = data_model.select_dtypes(np.number).columns\n",
    "    _ci = {column: None for column in numeric_cols}\n",
    "    for column in numeric_cols:\n",
    "        \n",
    "        data_model[column] = np.where(data[column]<=0, np.NAN, data_model[column]) \n",
    "        data_model[column] = data_model[column].fillna(data_model[column].mean())\n",
    "        transformed_data, ci = stats.boxcox(data[column])\n",
    "        data_model[column] = transformed_data\n",
    "        _ci[column] = [ci] \n",
    "    return data_model, _ci"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "03d89cb9",
   "metadata": {},
   "outputs": [],
   "source": [
    "def remove_outliers(data_model, threshold=1.5, in_columns=data_model.select_dtypes(np.number).columns, skip_columns=[]):\n",
    "    for column in in_columns:\n",
    "        if column not in skip_columns:\n",
    "            upper = np.percentile(data_model[column],75)\n",
    "            lower = np.percentile(data_model[column],25)\n",
    "            iqr = upper - lower\n",
    "            upper_limit = upper + (threshold * iqr)\n",
    "            lower_limit = lower - (threshold * iqr)\n",
    "            data_model = data_model[(data_model[column]>lower_limit) & (data_model[column]<upper_limit)]\n",
    "    return data_model"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "778de53e",
   "metadata": {},
   "outputs": [],
   "source": [
    "data_ratings.columns = [column.lower().replace('-', '_') for column in data_ratings.columns]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "56e91bc2",
   "metadata": {},
   "outputs": [],
   "source": [
    "books_final = data_books.drop(['image_url_s', 'image_url_m', 'image_url_l'],axis=1,inplace=True)"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.8"
  },
  "toc": {
   "base_numbering": 1,
   "nav_menu": {},
   "number_sections": true,
   "sideBar": true,
   "skip_h1_title": true,
   "title_cell": "Table of Contents",
   "title_sidebar": "Contents",
   "toc_cell": false,
   "toc_position": {},
   "toc_section_display": true,
   "toc_window_display": false
  },
  "varInspector": {
   "cols": {
    "lenName": 16,
    "lenType": 16,
    "lenVar": 40
   },
   "kernels_config": {
    "python": {
     "delete_cmd_postfix": "",
     "delete_cmd_prefix": "del ",
     "library": "var_list.py",
     "varRefreshCmd": "print(var_dic_list())"
    },
    "r": {
     "delete_cmd_postfix": ") ",
     "delete_cmd_prefix": "rm(",
     "library": "var_list.r",
     "varRefreshCmd": "cat(var_dic_list()) "
    }
   },
   "types_to_exclude": [
    "module",
    "function",
    "builtin_function_or_method",
    "instance",
    "_Feature"
   ],
   "window_display": false
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
