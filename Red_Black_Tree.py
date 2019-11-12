class Color:
    black = 0
    red = 1

class Node:
    def __init__(self,info=None,color=None):
        self.info = info
        self.color = color
        self.lchild = None
        self.rchild = None
        self.parent = None


class RBTree:
    def __init__(self):
        self.ext = Node(-1,Color.black) # nó externo
        self.root = self.ext # nao tem elementos presentes
        #insera valores na arvore 
    def insert(self,val):
        temp = Node()
        ptr = self.root
        par = self.ext
        while(ptr!=self.ext):
            par = ptr
            if ptr.info > val:
                ptr = ptr.lchild
            elif ptr.info < val:
                ptr = ptr.rchild
            else:
                print('Duplicate Element')
                return
        temp.info = val
        temp.lchild = self.ext
        temp.rchild = self.ext
        temp.color = Color.red
        temp.parent = par
        if par == self.ext:
            self.root = temp
        elif temp.info < par.info:
            par.lchild = temp
        else:
            par.rchild = temp
        self.balance_insert(temp)
        #faz o balanceamento apos a insercao 
    def balance_insert(self,ptr):
        while ptr.parent.color == Color.red:
            par = ptr.parent # parent
            grandPar = par.parent
            if par == grandPar.lchild:
                uncle = grandPar.rchild
                if uncle.color == Color.red:
                    par.color = Color.black
                    uncle.color = Color.black
                    grandPar.color = Color.red
                    ptr = grandPar
                else: # 'tio' da cor preta
                    if ptr == par.rchild:
                        self.rotate_left(par)
                        ptr = par
                        par = ptr.parent
                    par.Color = Color.black
                    grandPar.color = Color.red
                    self.rotate_right(grandPar)
            elif par == grandPar.rchild:
                uncle = grandPar.lchild
                if uncle.color == Color.red:
                    par.color = Color.black
                    uncle.color = Color.black
                    grandPar.color = Color.red
                    ptr = grandPar
                else: # 'tio' da cor preta
                    if ptr == par.lchild:
                        self.rotate_right(par)
                        ptr = par
                        par = ptr.parent
                    par.color = Color.black
                    grandPar.color = Color.red
                    self.rotate_left(grandPar)
            else:
                continue
        self.root.color = Color.black
        #procura na arvore um elemento(key) e retorna em forma de string true or false se achou ou nao
    def search(self,key,return_loc=False):
        ptr = self.root
        while ptr!=self.ext:
            if ptr.info == key:
                return ptr if return_loc else 'True'
            elif ptr.info < key:
                ptr = ptr.rchild
            else:
                ptr = ptr.lchild
        return ptr if return_loc else 'False'
        #deleta na arvore o elemento passado como paramentro 
    def delete(self,val):
        ptr = self.search(val,True)
        if ptr == self.ext:
            print('Element does not exist')
            return
        if ptr.lchild != self.ext or ptr.rchild != self.ext:
            succ = self.inorder_succ(ptr)
            ptr.info = succ.info
            ptr = succ
        if ptr.lchild != self.ext:
            child = ptr.lchild
        else:
            child = ptr.rchild
        child.parent = ptr.parent
        if ptr == self.root:
            self.root = child
        elif ptr.parent.lchild == ptr:
            ptr.parent.lchild = child
        else:
            ptr.parent.rchild = child
        if child == self.root:
            child.color = Color.black
        elif ptr.color == Color.black:
            if child != self.ext:
                child.color = Color.black
            else:
                self.balance_delete(child)
        else:
            pass
        #faz o balanceamento apos a remocao 
    def balance_delete(self,ptr):
        while ptr != self.root:
            if ptr.parent.lchild == ptr:
                sib = ptr.parent.rchild # irmao
                # 'irmao' vermelho
                if sib.color == Color.red:
                    sib.color = Color.black
                    ptr.parent.color = Color.red
                    self.rotate_left(ptr.parent)
                    sib = ptr.parent.rchild # novo irmao
                # ambos os sobrinhos sao pretos
                if sib.lchild.color == Color.black and sib.rchild.color == Color.black:
                    sib.color = Color.red
                    if ptr.parent.color == Color.red:
                        ptr.parent.color = Color.black
                        return
                    ptr = ptr.parent
                # no minimo um sobrinho preto
                else: #faz sobrinho mais longe ser vermelhor se ele for black
                    # making far nephew red if it is black
                    if sib.rchild.color == Color.black:
                        sib.lchild.color = Color.black
                        sib.color = Color.red
                        self.rotate_right(sib)
                        sib = ptr.parent.rchild # new irmao
                    sib.color = ptr.parent.color
                    ptr.parent.color = Color.black
                    sib.rchild.color = Color.black
                    self.rotate_left(ptr.parent)
                    return
            # o contrario da condicao a cima
            else:
                sib = ptr.parent.lchild
                if sib.color == Color.red:
                    sib.color = Color.black
                    ptr.parent.color = Color.red
                    self.rotate_right(ptr.parent)
                    sib = ptr.parent.lchild
                if sib.lchild.color == Color.black and sib.rchild.color == Color.black:
                    sib.color = Color.red
                    if ptr.parent.color == Color.red:
                        ptr.parent.color = Color.black
                        return
                    ptr = ptr.parent
                else:
                    if sib.lchild.color == Color.black:
                        sib.rchild.color = Color.black
                        sib.color = Color.red
                        self.rotate_left(sib)
                        sib = ptr.parent.lchild
                    sib.color = ptr.parent.color
                    ptr.parent.color = Color.black
                    sib.lchild.color = Color.black
                    self.rotate_right(ptr.parent)
                    return
                    
    def inorder_succ(self,ptr):
        ptr = ptr.rchild
        while ptr.lchild != self.ext:
            ptr = ptr.lchild
        return ptr
    def rotate_left(self,ptr):
        rptr = ptr.rchild # filho a direita
        ptr.rchild = rptr.lchild
        if rptr.lchild!=self.ext:
            rptr.lchild.parent = ptr
        rptr.parent = ptr.parent
        if ptr.parent == self.ext:
            self.root = rptr
        elif ptr == ptr.parent.lchild:
            ptr.parent.lchild = rptr
        else:
            ptr.parent.rchild = rptr
        rptr.lchild = ptr
        ptr.parent = rptr
    def rotate_right(self,ptr):
        lptr = ptr.lchild # filho a esquerda
        ptr.lchild = lptr.rchild
        if lptr.rchild!=self.ext:
            lptr.rchild.parent = ptr
        lptr.parent = ptr.parent
        if ptr.parent == self.ext:
            self.root = lptr
        elif ptr == ptr.parent.rchild:
            ptr.parent.rchild = lptr
        else:
            ptr.parent.lchild = lptr
        lptr.rchild = ptr
        ptr.parent = lptr
        #ordena a arvore 
    def inorder(self,ptr):
        if ptr!=self.ext:
            self.inorder(ptr.lchild)
            print(ptr.info,end=' ')
            self.inorder(ptr.rchild)
    def display(self,ptr):
        print(ptr.info,'Color = ',('Red' if ptr.color==1 else 'Black'))
        if ptr.lchild != self.ext:
            print(ptr.info,'left -> ',end='')
            self.display(ptr.lchild)
        if ptr.rchild != self.ext:
            print(ptr.info,'right -> ',end='')
            self.display(ptr.rchild)

r = RBTree()
def main():
    print("In order to balance the tree, you have to insert new numbers in your previously list, and use one of the choices below",end='')
    print('Enter initial elements :')
    for ele in list(map(int,input().split())):
        r.insert(ele)
    print('1.Insert','2.Inorder','3.Search','4.Delete','5.Display',sep='\n')
    while True:
        choice = int(input())
        if choice == 1:
            print('Enter element to be inserted : ',end='')
            r.insert(int(input()))
        elif choice == 2:
            print('Inorder : ',end='')
            r.inorder(r.root)
            print()
        elif choice == 3:
            print('Enter search element : ',end='')
            print(r.search(int(input())))
        elif choice == 4:
            print('Enter element to be deleted : ',end='')
            r.delete(int(input()))
        elif choice == 5:
            if r.root == r.ext:
                print('Tree is empty')
            else:
                print('Root -> ',end='')
                r.display(r.root)
        else:
            break


if __name__ == '__main__':
    main()