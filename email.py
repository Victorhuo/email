import os


def email_reader(email_path):
    punctuations = """,.<>()*&^%$#@!'";~`[]{}|、\\/~+_-=?"""
    with open(email_path, "r", encoding="utf-8") as f:
        content_list = f.readlines()
    content = (" ".join(content_list)).replace("\r\n", " ").replace("\t", " ")
    clean_word = []
    for punctuation in punctuations:
        content = (" ".join(content.split(punctuation))).replace("  ", " ")
        clean_word = [word.lower() for word in content.split(" ") if len(word) > 2]
    return clean_word


def get_word(email_file):
    word_list = []
    word_set = []
    fileArray = []
    for root, dirs, files in os.walk(email_file):
        for fn in files:
            eachpath = str(root + "\\" + fn)
            fileArray.append(eachpath)
    for email_path in fileArray:
        clean_word = email_reader(email_path)
        word_list.append(clean_word)
        word_set.extend(clean_word)
    return word_list, set(word_set)


def count_word_prob(email_list, union_set):
    word_prob = {}
    for word in union_set:
        counter = 0
        for email in email_list:
            if word in email:
                counter += 1
            else:
                continue
        prob = 0.0
        if counter != 0:
            prob = counter / len(email_list)
        else:
            prob = 0.01
        word_prob[word] = prob
    return word_prob


def filter(ham_word_pro, spam_word_pro, test_file):
    test_paths = []
    for root, dirs, files in os.walk(test_file):
        for fn in files:
            eachpath = str(root + "\\" + fn)
            test_paths.append(eachpath)
    for test_path in test_paths:
        email_spam_prob = 0.0
        spam_prob = 0.5
        ham_prob = 0.5
        file_name = test_path.split("\\")[-1]
        prob_dict = {}
        words = set(email_reader(test_path))
        for word in words:
            Psw = 0.0
            if word not in spam_word_pro:
                Psw = 0.4
            else:
                Pws = spam_word_pro[word]
                Pwh = ham_word_pro[word]
                Psw = spam_prob * (Pws / (Pwh * ham_prob + Pws * spam_prob))
            prob_dict[word] = Psw
        numerator = 1
        denominator_h = 1
        for k, v in prob_dict.items():
            numerator *= v
            denominator_h *= 1 - v
        email_spam_prob = round(numerator / (numerator + denominator_h), 4)
        if email_spam_prob > 0.5:
            print(file_name, "spam", email_spam_prob)
        else:
            print(file_name, "ham", email_spam_prob)


def main():
    ham_file = r"D:\cncpp\python\ai\two\email\ham"
    spam_file = r"D:\cncpp\python\ai\two\email\spam"
    test_file = r"D:\cncpp\python\ai\two\email\test"
    ham_list, ham_set = get_word(ham_file)
    spam_list, spam_set = get_word(spam_file)
    union_set = ham_set | spam_set
    ham_word_pro = count_word_prob(ham_list, union_set)
    spam_word_pro = count_word_prob(spam_list, union_set)
    filter(ham_word_pro, spam_word_pro, test_file)


main()
