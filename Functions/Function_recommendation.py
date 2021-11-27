{
 "cells": [
  {
   "cell_type": "markdown",
   "id": "a87f5aaa",
   "metadata": {},
   "source": [
    "# _Function : Recommendation system_"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "51bab1c6",
   "metadata": {},
   "outputs": [],
   "source": [
    "def findksimilarusers(user_id, ratings, metric = metric, k=k):\n",
    "    similarities=[]\n",
    "    indices=[]\n",
    "    model_knn = NearestNeighbors(metric = metric, algorithm = 'brute') \n",
    "    model_knn.fit(ratings)\n",
    "    loc = ratings.index.get_loc(user_id)\n",
    "    distances, indices = model_knn.kneighbors(ratings.iloc[loc, :].values.reshape(1, -1), n_neighbors = k+1)\n",
    "    similarities = 1-distances.flatten()\n",
    "            \n",
    "    return similarities,indices"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "65fb8d99",
   "metadata": {},
   "outputs": [],
   "source": [
    "def predict_userbased(user_id, item_id, ratings, metric = metric, k=k):\n",
    "    prediction=0\n",
    "    user_loc = ratings.index.get_loc(user_id)\n",
    "    item_loc = ratings.columns.get_loc(item_id)\n",
    "    similarities, indices=findksimilarusers(user_id, ratings,metric, k) #similar users based on cosine similarity\n",
    "    mean_rating = ratings.iloc[user_loc,:].mean() #to adjust for zero based indexing\n",
    "    sum_wt = np.sum(similarities)-1\n",
    "    product=1\n",
    "    wtd_sum = 0 \n",
    "    \n",
    "    for i in range(0, len(indices.flatten())):\n",
    "        if indices.flatten()[i] == user_loc:\n",
    "            continue;\n",
    "        else: \n",
    "            ratings_diff = ratings.iloc[indices.flatten()[i],item_loc]-np.mean(ratings.iloc[indices.flatten()[i],:])\n",
    "            product = ratings_diff * (similarities[i])\n",
    "            wtd_sum = wtd_sum + product\n",
    "    \n",
    "    #in case of very sparse datasets, using correlation metric for collaborative based approach may give negative ratings\n",
    "    #which are handled here as below\n",
    "    if prediction <= 0:\n",
    "        prediction = 1   \n",
    "    elif prediction >10:\n",
    "        prediction = 10\n",
    "    \n",
    "    prediction = int(round(mean_rating + (wtd_sum/sum_wt)))\n",
    "    print ('\\nPredicted rating for user {0} -> item {1}: {2}'.format(user_id,item_id,prediction))\n",
    "\n",
    "    return prediction"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "e54a6cc2",
   "metadata": {},
   "outputs": [],
   "source": [
    "def suppress_stdout():\n",
    "    with open(os.devnull, \"w\") as devnull:\n",
    "        old_stdout = sys.stdout\n",
    "        sys.stdout = devnull\n",
    "        try:  \n",
    "            yield\n",
    "        finally:\n",
    "            sys.stdout = old_stdout"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "21ae28af",
   "metadata": {},
   "outputs": [],
   "source": [
    "def recommendItem(user_id, ratings, metric=metric):    \n",
    "    if (user_id not in ratings.index.values) or type(user_id) is not int:\n",
    "        print (\"Choose a User_id from this list :\\n\\n {} \".format(re.sub('[\\[\\]]', '', np.array_str(ratings_matrix.index.values))))\n",
    "    else:    \n",
    "        ids = ['Item-based (correlation)','Item-based (cosine)','User-based (correlation)','User-based (cosine)']\n",
    "        select = widgets.Dropdown(options=ids, value=ids[0],description='Select approach', width='1000px')\n",
    "        def on_change(change):\n",
    "            clear_output(wait=True)\n",
    "            prediction = []            \n",
    "            if change['type'] == 'change' and change['name'] == 'value':            \n",
    "                if (select.value == 'Item-based (correlation)') | (select.value == 'User-based (correlation)') :\n",
    "                    metric = 'correlation'\n",
    "                else:                       \n",
    "                    metric = 'cosine'   \n",
    "                with suppress_stdout():\n",
    "                    if (select.value == 'Item-based (correlation)') | (select.value == 'Item-based (cosine)'):\n",
    "                        for i in range(ratings.shape[1]):\n",
    "                            if (ratings[str(ratings.columns[i])][user_id] !=0): #not rated already\n",
    "                                prediction.append(predict_itembased(user_id, str(ratings.columns[i]) ,ratings, metric))\n",
    "                            else:                    \n",
    "                                prediction.append(-1) #for already rated items\n",
    "                    else:\n",
    "                        for i in range(ratings.shape[1]):\n",
    "                            if (ratings[str(ratings.columns[i])][user_id] !=0): #not rated already\n",
    "                                prediction.append(predict_userbased(user_id, str(ratings.columns[i]) ,ratings, metric))\n",
    "                            else:                    \n",
    "                                prediction.append(-1) #for already rated items\n",
    "                prediction = pd.Series(prediction)\n",
    "                prediction = prediction.sort_values(ascending=False)\n",
    "                recommended = prediction[:10]\n",
    "                print (\"As per {0} approach....Following books are recommended...\".format(select.value))\n",
    "                for i in range(len(recommended)):\n",
    "                     print (\"{0}. {1}\".format(i+1,books.bookTitle[recommended.index[i]].encode('utf-8')))                        \n",
    "        select.observe(on_change)\n",
    "        display(select)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "2505c94c",
   "metadata": {},
   "outputs": [],
   "source": []
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
