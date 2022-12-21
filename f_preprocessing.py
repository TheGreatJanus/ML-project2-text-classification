{"metadata":{"kernelspec":{"language":"python","display_name":"Python 3","name":"python3"},"language_info":{"pygments_lexer":"ipython3","nbconvert_exporter":"python","version":"3.6.4","file_extension":".py","codemirror_mode":{"name":"ipython","version":3},"name":"python","mimetype":"text/x-python"}},"nbformat_minor":4,"nbformat":4,"cells":[{"cell_type":"code","source":"# %% [code]\nimport numpy as np # linear algebra\nimport pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)\nimport os\n\nimport nltk\nfrom nltk.corpus import stopwords\nfrom nltk.stem.snowball import SnowballStemmer\nfrom nltk.stem.porter  import PorterStemmer\nfrom nltk.stem import WordNetLemmatizer\n\nfrom wordcloud import WordCloud\n\nimport pandas as pd\nimport random, time\nfrom babel.dates import format_date, format_datetime, format_time\nimport numpy as np\nimport seaborn as sns\nimport matplotlib.pyplot as plt\n\nimport sklearn\nfrom sklearn.linear_model import LogisticRegression\nfrom sklearn.model_selection import train_test_split, GridSearchCV\nfrom sklearn.pipeline import Pipeline\nfrom sklearn.feature_extraction.text import TfidfVectorizer\nfrom sklearn.utils.class_weight import compute_class_weight\nfrom sklearn.metrics import classification_report, accuracy_score\nfrom sklearn.feature_extraction.text import CountVectorizer\nfrom sklearn.decomposition import PCA\nfrom sklearn.decomposition import TruncatedSVD\n\n# %% [markdown]\n# # Preprocessing functions\n\n# %% [code]\ndef import_data(path_dataset_neg, path_dataset_pos):\n    \"\"\"\n    This function imports the data set, adds labels and returns a Pandas Dataframe, without duplicates. \n    Input : path of negative data set, path of postive dataset \n    Output: Pandas data frame with two columns : text and label\n    \"\"\"\n\n    #Kaggle version\n    train_neg = [tweet[:-1] for tweet in open(path_dataset_neg).readlines()]\n    train_pos = [tweet[:-1] for tweet in open(path_dataset_pos).readlines()]\n        \n    X, y = train_neg + train_pos, [-1 for i in range(len(train_neg))]+[1 for i in range(len(train_pos))]\n    df = pd.DataFrame(list(zip(y, X)), columns = ['label','text'], dtype = str)\n    df.drop_duplicates(inplace = True)# Delete duplicate Tweets\n    df['label'] = df['label'].astype(int)\n    \n    return df\n    \n    \n\n# %% [code]\ndef cleaning_data(df):\n    \"\"\"\n    This function removes special characters, numbers, url links, single characters  \n    Input : Pandas data frame with two columns : text and label \n    Output: Pandas data frame with two columns : text and label\n    \"\"\"\n    \n    # remove special characters from text column\n    df.text = df.text.str.replace('[#,@,&]', '')\n    \n    #Replace special characters\n    df.text = df.text.str.replace('(','')\n    df.text = df.text.str.replace(')','')\n    df.text = df.text.str.replace('=','')\n    df.text = df.text.str.replace('!','')\n    df.text = df.text.str.replace('?','')\n    df.text = df.text.str.replace('\"','')\n    df.text = df.text.str.replace('_','')\n    df.text = df.text.str.replace('-','')\n    df.text = df.text.str.replace(',','')\n    df.text = df.text.str.replace('.','')\n    df.text = df.text.str.replace(';','')\n    df.text = df.text.str.replace('+','')\n    df.text = df.text.str.replace('<user>','')\n    df.text = df.text.str.replace('<rt>','')\n    df.text = df.text.str.replace(':','')\n    df.text = df.text.str.replace('/','')\n    df.text = df.text.str.replace('<','')\n    df.text = df.text.str.replace('>','')\n    df.text = df.text.str.replace('\\'s','')\n    \n    # Remove digits\n    df.text = df.text.str.replace('\\d*','')\n    \n    #Remove www\n    df.text = df.text.str.replace('w{3}','')\n    # remove urls\n    df.text = df.text.str.replace(\"http\\S+\", \"\")\n    # remove multiple spaces with single space\n    df.text = df.text.str.replace('\\s+', ' ')\n    #remove all single characters (except \"i\")\n    df.text = df.text.str.replace(r'\\s+[a-hA-H]\\s+', '')\n    df.text = df.text.str.replace(r'\\s+[j-zJ-Z]\\s+', '')\n    df.text = df.text.str.replace(r'\\s+[i-iI-I]\\s+',' ')\n    return df\n\n\n# %% [code]\ndef remove_stopwords(df):\n    \n    \"\"\"\n    This function stopwords, defined in the list in the function.\n    We delete Twitter specific words, english stopwords, but we keep negative forms of verbs and negative adverbs\n    Input : Pandas data frame with two columns : text and label \n    Output: Pandas data frame with two columns : text and label\n    \"\"\"\n    \n    stop_words = ['i', 'me', 'my', 'myself', 'we','url' 'our', 'ours', 'ourselves', 'you', \"you're\", \"you've\", \"you'll\", \"you'd\", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', \"she's\", 'her', 'hers', 'herself', 'it', \"it's\", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', \"that'll\", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', \"don't\", 'should', \"should've\", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain']\n    stop_words.extend(['u', 'wa', 'ha','ho', 'would', 'com', 'user','<user>', '<rt>' 'url', 'rt', 'custom picture', 'i\\'m', 'picture frame','<url>', 'positer frame', 'x','i\\'ll'])\n    stop_words.remove('not')\n    stop_words.remove('no')\n    stop_words.remove('nor')\n    df['text'] = df['text'].apply(lambda x: ' '.join([word for word in x.split() if word not in (stop_words)]))\n    return df\n\n\n\n# %% [code]\ndef Porter_stemmer(df):\n    \"\"\"\n    This function applies Porter Stemmer methodology to reduces words to their stem\n    Input : Pandas data frame with two columns : text and label \n    Output: Pandas data frame with two columns : text and label\n    \"\"\"   \n    stemmer = PorterStemmer()\n    df['text'] = df['text'].apply(lambda x: ' '.join([stemmer.stem(word) for word in x.split()]))\n    return df\n\ndef snow_ball_stemmer(df):\n    \"\"\"\n    This function applies Snowball Stemmer methodology to reduces words to their stem\n    Input : Pandas data frame with two columns : text and label \n    Output: Pandas data frame with two columns : text and label\n    \"\"\"   \n    snow_stemmer = SnowballStemmer(language='english')\n    df['text'] = df['text'].apply(lambda x: ' '.join([snow_stemmer.stem(word) for word in x.split()]))\n    return df\n\ndef lemmatize_text(df):\n    \"\"\"\n    This function applies World Net Lemmatizing methodology to reduces words to their stem\n    Input : Pandas data frame with two columns : text and label \n    Output: Pandas data frame with two columns : text and label\n    \"\"\"   \n    lemmatizer = nltk.stem.WordNetLemmatizer()\n    df['text'] = df['text'].apply(lambda x: ' '.join([lemmatizer.lemmatize(word) for word in x.split()]))\n    return df\n\n# %% [markdown]\n# # Vectorizer\n\n# %% [code]\ndef Basic_Vectorizer(df):\n    \"\"\"\n    This function transforms text into a matrix mapping X using all words in text as vocabulary list \n    It also transform the labels to a numpy vector y\n    Input : Pandas data frame with two columns : text and label \n    Output:  X vector of features, y vector of labels\n    \"\"\"   \n    text = df['text']\n    y = df['label'].to_numpy()\n    \n    basic_vectorizer = CountVectorizer(binary=True)\n    basic_vectorizer.fit(text)\n    X = basic_vectorizer.transform(text)\n    \n    return X, y\n\n\n\ndef N_Gram_Vectorizer(df, N):\n    \"\"\"\n    This function transforms text into a matrix mapping X using all words in text as vocabulary list.\n    It maps N-grams (series of N consecutive words)\n    It also transform the labels to a numpy vector y\n    Input : Pandas data frame with two columns : text and label, N the parameter for N-grams \n    Output:  X vector of features, y vector of labels\n    \"\"\"   \n    text = df['text']\n    y = df['label'].to_numpy()\n    \n    #adding two or three word sequences (bigrams or trigrams)\n    ngram_vectorizer = CountVectorizer(binary=True, ngram_range=(1, N))\n    ngram_vectorizer.fit(text)\n    X = ngram_vectorizer.transform(text)\n    \n    return X, y\n\n# %% [markdown]\n# # SVD\n\n# %% [code]\ndef SVD_preprocessing(X, y, N):\n    \n     \"\"\"\n    This function applies SVD transformation to the features matrix X, keeping the N most significant drivers\n    Input : Matrix of features X, vector of labels y, parameter N for number of drivers to keep\n    Output:  X vector of features after SVD, y vector of labels\n    \"\"\"  \n    clf = TruncatedSVD(100)\n    X_SVD = clf.fit_transform(X)\n    \n    return X_SVD, y\n\n# %% [markdown]\n# # Preprocessing methods for testing\n\n# %% [code]\ndef evaluate_method(X,y, message):\n    \"\"\"\n    This function first splits the data X, y into training and testing sets\n    It then trains and test with a Logistic regression model and display the score\n    Input : Matrix of features X, vector of labels y, message to display\n    Output:  Nonen, but prints accuracy of model\n    \"\"\"   \n    random.seed(42)\n    X_train, X_val, y_train, y_val = train_test_split(X, y, train_size = 0.75)\n    lr = LogisticRegression()\n    lr.fit(X_train, y_train)\n    print (\"Accuracy \"+message+\" : %s\" % (accuracy_score(y_val, lr.predict(X_val))))\n    return None\n\n# %% [code]\ndef test_clean_data(path_dataset_neg, path_dataset_pos):\n    \n    \"\"\"\n    This function compares the accuracy of a logistic model, with and without a given processing method : cleaning data\n    Input : path of negative data set, path of postive dataset\n    Output:  Nonen, but prints accuracy of different processing method\n    \"\"\"   \n    \n    #Prediction accuracy with clean data\n    df1 = import_data(path_dataset_neg, path_dataset_pos)\n    df1 = cleaning_data(df1)\n    X1, y1 = Basic_Vectorizer(df1)\n    evaluate_method(X1, y1, \"with clean data\")\n    \n    #Prediction accuracy without clean data\n    \n    df2 = import_data(path_dataset_neg, path_dataset_pos)\n    X2, y2 = Basic_Vectorizer(df2)\n    evaluate_method(X2, y2, \"without clean data\")\n    \n    #Solution of test\n    \n    #Accuracy with clean data : 0.7924378460656063\n    #Accuracy without clean data : 0.7940041031523681\n    #As the Accuracy is equal, we keep this process\n    \n    return None\n\n# %% [code]\ndef test_stopwords(path_dataset_neg, path_dataset_pos):\n    \"\"\"\n    This function compares the accuracy of a logistic model, with and without a given processing method : stopwords\n    We keep the methods : cleaning data,  that are relevant according to the precedant test\n    Input : path of negative data set, path of postive dataset\n    Output:  None, but prints accuracy of different processing method\n    \"\"\"   \n    \n    #Prediction accuracy with  deleting stopwords\n    df1 = import_data(path_dataset_neg, path_dataset_pos)\n    df1 = cleaning_data(df1)\n    df1 = remove_stopwords(df1)\n    X1, y1 = Basic_Vectorizer(df1)\n    evaluate_method(X1, y1, \"with deleting stopwords\")\n    \n    #Prediction accuracy without deleting stopwords\n    \n    df2 = import_data(path_dataset_neg, path_dataset_pos)\n    df2 = cleaning_data(df2)\n    X2, y2 = Basic_Vectorizer(df2)\n    evaluate_method(X2, y2, \"without deleting stopwords\")\n    \n    #Solution of test\n    \n    #Accuracy with deleting stopwords : 0.7828858838322561\n    #Accuracy without deleting stopwords : 0.790011250579074\n    #As the Accuracy is equal, we should not keep this process\n    \n    \n    return None\n\n\n# %% [code]\ndef test_normalization(path_dataset_neg, path_dataset_pos):\n     \"\"\"\n    This function compares the accuracy of a logistic model, with and without a given processing method : normalization methods : Porter Stemming, Snowball stemming, Lemmatizing\n    We keep the methods : cleaning data, remove stopwords, that are relevant according to the precedant test\n    Input : path of negative data set, path of postive dataset\n    Output:  None, but prints accuracy of different processing method\n    \"\"\"  \n    \n    #Prediction accuracy without  deleting normalization\n    df1 = import_data(path_dataset_neg, path_dataset_pos)\n    df1 = cleaning_data(df1)\n    df1 = remove_stopwords(df1)#voir si on garde\n    X1, y1 = Basic_Vectorizer(df1)\n    evaluate_method(X1, y1, \"without normalization\")\n    \n    #Prediction accuracy with Porter\n    df2 = import_data(path_dataset_neg, path_dataset_pos)\n    df2 = cleaning_data(df2)\n    df2 = remove_stopwords(df2) #voir si on garde\n    df2 = Porter_stemmer(df2)\n    X2, y2 = Basic_Vectorizer(df2)\n    evaluate_method(X2, y2, \"with Porter Stemmer\")\n    \n    \n    #Prediction accuracy with SnowBall Stemmer\n    df3 = import_data(path_dataset_neg, path_dataset_pos)\n    df3 = cleaning_data(df3)\n    df3 = remove_stopwords(df3) #voir si on garde\n    df3 = snow_ball_stemmer(df3)\n    X3, y3 = Basic_Vectorizer(df3)\n    evaluate_method(X3, y3, \"with Snowball Stemmer\")   \n    \n    \n    #Prediction accuracy with Lemmatizer\n    df4 = import_data(path_dataset_neg, path_dataset_pos)\n    df4 = cleaning_data(df4)\n    df4 = remove_stopwords(df4) #voir si on garde\n    df4 = lemmatize_text(df4)\n    \n    X4, y4 = Basic_Vectorizer(df4)\n    evaluate_method(X4, y4, \"with lemmatization\")   \n    \n    \n    #Solution of test\n    \n    #Accuracy without normalization : 0.782091725309391\n    #Accuracy with Porter Stemmer : 0.7836359224371843\n    #Accuracy with Snowball Stemmer : 0.7831285433809093\n    #Accuracy with lemmatization : XXX\n    #As the Accuracy is nearly equal, we keep method Porter Stemmer, that is the best for reproductibility of results and is short to implement\n    \n    return None\n\n\n# %% [code]\ndef test_vectorization(path_dataset_neg, path_dataset_pos):\n    \n     \"\"\"\n    This function compares the accuracy of a logistic model, with and without a given vectorization method : 2-Grams, 3-Grams.\n    We keep the methods : cleaning data, remove stopwords and Porter Stemmer, that are relevant according to the precedant test\n    Input : path of negative data set, path of postive dataset\n    Output:  None, but prints accuracy of different processing method\n    \"\"\"  \n    \n    #Prediction accuracy with basic vectorization\n    df1 = import_data(path_dataset_neg, path_dataset_pos)\n    df1 = cleaning_data(df1)\n    df1 = remove_stopwords(df1)#voir si on garde\n    df1 = Porter_stemmer(df1)\n    X1, y1 = Basic_Vectorizer(df1)\n    evaluate_method(X1, y1, \"with basic vectorization\")\n    \n    \n    #Prediction accuracy with 2-Grams vectorization\n    df1 = import_data(path_dataset_neg, path_dataset_pos)\n    df1 = cleaning_data(df1)\n    df1 = remove_stopwords(df1)#voir si on garde\n    df1 = Porter_stemmer(df1)\n    X1, y1 = N_Gram_Vectorizer(df1,2)\n    evaluate_method(X1, y1, \"with 2-grams vectorization\")\n    \n    \n    \n    #Prediction accuracy with 3-Grams vectorization\n    df1 = import_data(path_dataset_neg, path_dataset_pos)\n    df1 = cleaning_data(df1)\n    df1 = remove_stopwords(df1)#voir si on garde\n    df1 = Porter_stemmer(df1)\n    X1, y1 = N_Gram_Vectorizer(df1,3)\n    evaluate_method(X1, y1, \"with 3-grams vectorization\")\n    \n    \n    #Solution of test\n    \n    #Accuracy with basic vectorization : 0.7799739692484172\n    #Accuracy with 2-grams vectorization : 0.7945776620855485\n    #Accuracy with 3-grams vectorization : 0.7926143257373541\n    \n\n    return None\n\n\n# %% [code]\ndef test_SVD(path_dataset_neg, path_dataset_pos, N):\n     \"\"\"\n    This function compares the accuracy of a logistic model, with and without a given processing method : SVD \n    We keep the methods : cleaning data, remove stopwords and Porter Stemmer, 2-Grams Vectorizer that are relevant according to the precedant test\n    Input : path of negative data set, path of postive dataset, Dimension of residual training set \n    Output:  Nonen, but prints accuracy of different processing method\n    \"\"\"  \n    \n    #Prediction accuracy with basic vectorization\n    df1 = import_data(path_dataset_neg, path_dataset_pos)\n    df1 = cleaning_data(df1)\n    df1 = remove_stopwords(df1)#voir si on garde\n    df1 = Porter_stemmer(df1)\n    X1, y1 = N_Gram_Vectorizer(df1,2)\n    X1, y1 = SVD_preprocessing(X1, y1, N)\n    message = \"with PCA \" +str(N)\n    evaluate_method(X1, y1, message)\n    return None\n\n#Accuracy with PCA 10 000 : 0.7068010853499812\n","metadata":{"_uuid":"d0fb97b0-dc51-484d-b5dc-5c3be897f12f","_cell_guid":"6852d67e-d8ed-42e8-8d86-15d09c741030","collapsed":false,"jupyter":{"outputs_hidden":false},"trusted":true},"execution_count":null,"outputs":[]}]}