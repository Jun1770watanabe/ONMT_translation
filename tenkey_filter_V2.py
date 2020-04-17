class KeyinputFilter:
    """ 疑似的な入力を作成する際に利用するフィルタ
    1 ローマ字キー入力文字列を数字列に置き換えるフィルタ
    2 かな文字列をローマ字キー入力文字列に置き換えるフィルタ
    """

    _KEYIN2NUMBER_TABLE = str.maketrans(
        '1qaz2wsx3edc4rfvtgbyhn7ujm8ik9ol0p-',
        '11112222333344444447777777888999000')

    @classmethod
    def alphab2num(cls, text):
        # exchange upper case to lower case
        text = text.lower()

        # convert alphabet to number
        numseq = text.translate(cls._KEYIN2NUMBER_TABLE)
        return numseq
