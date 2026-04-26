import cv2
import numpy as np
import time




class TicTacToe(object):
    def __init__(self):
        self.width = 800
        self.height = 800
        self.state = "page1"
        self.mode = 0
        self.chess = 0 # 0 for O, 1 for X
        self.press = 0
        self.press_time = 0
        self.current_player = 0 #0 for p1, 1 for p2
        self.board = np.array([[-1,-1,-1],
                               [-1,-1,-1],
                               [-1,-1,-1]])
        self.move_history = []
        self.game_over = 0
        self.winner = 0
        cv2.namedWindow("tic-tac-toe")
    def refresh(self):
        self.state = "page1"
        self.mode = 0
        self.chess = 0  # 0 for O, 1 for X
        self.press = 0
        self.current_player = 0  # 0 for p1, 1 for p2
        self.board = np.array([[-1, -1, -1],
                               [-1, -1, -1],
                               [-1, -1, -1]])
        self.game_over = 0
        self.move_history = []
        self.winner = 0
    def page3_init(self):
        self.current_player = 0  # 0 for p1, 1 for p2
        self.board = np.array([[-1, -1, -1],
                               [-1, -1, -1],
                               [-1, -1, -1]])
        self.game_over = 0
        self.move_history = []
        self.winner = 0

    def undo(self):
        if self.mode == 0:  # 双人对战模式
            # 只撤销一步
            row, col, player = self.move_history.pop()
            self.board[row][col] = -1
            self.current_player = player
        else:  # 人机对战模式
            # 需要连续撤销两步（人类的一步和AI的一步）
            if len(self.move_history) >= 2:
                # 撤销AI的走棋
                row1, col1, player1 = self.move_history.pop()
                self.board[row1][col1] = -1

                # 撤销人类的走棋
                row2, col2, player2 = self.move_history.pop()
                self.board[row2][col2] = -1

                # 设置轮到人类
                self.current_player = 0
    def move_chess(self,row,col):
        if self.board[row][col] != -1:
            return False
        else:
            self.move_history.append([row, col, self.current_player])  # 记录下来以用于悔棋
            if self.current_player == 0: #p1
                self.board[row][col] = self.chess
            else:
                if self.chess == 1: # p1选的是x,p2就下o
                    self.board[row][col] = 0
                elif self.chess == 0: # p1选的是0，p2就下x
                    self.board[row][col] = 1

        if self.current_player == 0:
            self.current_player = 1
        else:
            self.current_player = 0

        return True
    def check_win(self):
        for row in range(0,3):#检查行
            if self.board[row][0] == self.board[row][1] == self.board[row][2] != -1:
                if self.board[row][0] == self.chess:
                    self.game_over = 1
                    return 1
                else:
                    self.game_over = 1
                    return 2
        for col in range(0,3):#检查列
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != -1:
                if self.board[0][col] == self.chess:
                    self.game_over = 1
                    return 1
                else:
                    self.game_over = 1
                    return 2
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != -1:#对角线1
            if self.board[0][0] == self.chess:
                self.game_over = 1
                return 1
            else:
                self.game_over = 1
                return 2
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != -1:#对角线2
            if self.board[0][2] == self.chess:
                self.game_over = 1
                return 1
            else:
                self.game_over = 1
                return 2
        for row in range(0,3):
            for col in range(0,3):
                if self.board[row][col] == -1:
                    return -1 #继续
        self.game_over = 1
        return 0 #平局

    def evaluate_score(self,player_chess,ai_chess):
        for row in range(0, 3):  # 检查行
            if self.board[row][0] == self.board[row][1] == self.board[row][2] != -1:
                if self.board[row][0] == player_chess:
                    return 10
                elif self.board[row][0] == ai_chess:
                    return -10
        for col in range(0, 3):  # 检查列
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != -1:
                if self.board[0][col] == player_chess:
                    return 10
                elif self.board[0][col] == ai_chess:
                    return -10
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != -1:  # 对角线1
            if self.board[0][0] == player_chess:
                return 10
            elif self.board[0][0] == ai_chess:
                return -10
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != -1:  # 对角线2
            if self.board[0][2] == player_chess:
                return 10
            elif self.board[0][2] == ai_chess:
                return -10

        return 0  # 未分出胜负
    def is_full(self):
        for row in range(0, 3):
            for col in range(0, 3):
                if self.board[row][col] == -1:
                    return False  # 继续
        return True
    def minimax(self, is_turn,depth, player_chess,ai_chess,alpha=-float('inf'), beta=float('inf')):#返回的是对应分数
        score = self.evaluate_score(player_chess,ai_chess)
        if score == 10:
            return score-depth
        elif score == -10:
            return score+depth
        if self.is_full():
            return 0#平局
        if is_turn:#人类回合，max层
            best_score = -float('inf')
            for row in range(0, 3):
                for col in range(0, 3):
                    if self.board[row][col] == -1:
                        self.board[row][col] = player_chess#尝试走一步
                        score = self.minimax(0,depth+1,player_chess, ai_chess, alpha, beta)#通过递归算分数
                        self.board[row][col] = -1#撤销这一步
                        best_score = max(score, best_score)
                        #alpha-beta剪枝
                        alpha = max(alpha, best_score)
                        if beta <= alpha:
                            break

            return best_score
        else:#ai回合
            best_score = float('inf')
            for row in range(0, 3):
                for col in range(0, 3):
                    if self.board[row][col] == -1:
                        self.board[row][col] = ai_chess
                        score = self.minimax(1,depth+1,player_chess, ai_chess, alpha, beta)
                        self.board[row][col] = -1
                        best_score = min(score, best_score)
                        beta = min(beta, best_score)
                        if beta <= alpha:
                            break
            return best_score
    def best_move(self,player_chess,ai_chess):#ai的落棋点
        best_score = float('inf')
        best_move = (-1,-1)#对于井字棋而言，中心点是收益最大的点
        empty_pos = 0
        for row in range(0, 3):
            for col in range(0, 3):
                if self.board[row][col] == -1:
                    empty_pos += 1
        ''' 
        开局优化:
        如果是空棋盘(第一步)，不用运行复杂的Minimax
        井字棋最优第一步：中心 > 角落 > 边
        这里直接返回中心或角落，提高效率
        '''
        if empty_pos == 9:
            if self.board[1][1] == -1:
                return best_move
            else:
                corner = [(0,0),(0,2),(2,0),(2,2)]
                for row,col in corner:
                    if self.board[row][col] == -1:
                        best_move = (row,col)
                        return best_move
                return 0
        else:
            #采用标准minimax算法
            for row in range(0, 3):
                for col in range(0, 3):
                    if self.board[row][col] == -1:
                        self.board[row][col] = ai_chess
                        score = self.minimax(1,0,player_chess, ai_chess)
                        self.board[row][col] = -1
                        if score < best_score:
                            best_score = score
                            best_move = (row,col)
            return best_move
    #可能有问题需要改
    def ai_move(self):
        player_chess,ai_chess = -1,-1

        if self.game_over or self.current_player != 1:
            return  False

        if self.mode == 1:
            if self.chess == 1:
                ai_chess = 0
                player_chess = 1
            elif self.chess == 0:
                ai_chess = 1
                player_chess = 0
        else:
            return False
        best_move = self.best_move(player_chess,ai_chess)
        row,col = best_move
        pos = self.move_chess(row,col)
        return pos


    def page1(self):
        img = np.ones((self.height, self.width, 3), dtype=np.uint8) * 255
        cv2.putText(img,text = "Tic-Tac-Toe",org = (int(0.2*self.width),int(0.15*self.height)),
                    fontFace = cv2.FONT_HERSHEY_PLAIN,fontScale = 4,lineType = 4,thickness = 4,color = (0,0,0),)
        current_time = time.time()
        # p1 vs p2
        x1,y1 = 200,250
        pt1 = (x1,y1)
        x2,y2 = 580,350
        pt2 = (x2, y2)
        #点击效果动画
        if self.press == "p1vsp2" :
            time_passed = current_time - self.press_time
            if time_passed < 0.2:
                offset = int(5 * (1 - time_passed / 0.2))
                cv2.rectangle(img, (x1 + offset, y1 + offset), (x2 + offset, y2 + offset), (180, 180, 180), -1)
                cv2.line(img, (x1+offset,y1+offset), (x2+offset,y1+offset), (100, 100, 100), 4)
                cv2.line(img, (x1+offset,y1+offset), (x1+offset,y2+offset), (100, 100, 100), 4)
                cv2.line(img, (x1+offset,y2+offset), (x2+offset,y2+offset), (220, 220, 220), 4)
                cv2.line(img, (x2+offset,y2+offset), (x2+offset,y1+offset), (220, 220, 220), 4)


                cv2.putText(img, text="P1 vs P2", org=(x1 + 10 + offset, y1 + 70 + offset), fontFace=cv2.FONT_HERSHEY_PLAIN,
                            fontScale=4, lineType=4, thickness=4, color=(0, 0, 0), )
            else:
                self.state = "page2"
        else:#正常状态
            cv2.rectangle(img, pt1, pt2, (0, 0, 0), 8)
            cv2.rectangle(img, pt1, pt2, (200, 200, 200), -1)
            cv2.putText(img, text="P1 vs P2", org=(x1 + 10, y1 + 70), fontFace=cv2.FONT_HERSHEY_PLAIN,
                        fontScale=4, lineType=4, thickness=4, color=(0, 0, 0), )
        #p1 vs cpu
        y1 = y1+250
        pt1 = (x1, y1)
        y2 = y2+250
        pt2 = (x2, y2)
        if self.press == "p1vsCpu" :
            time_passed = current_time - self.press_time
            if time_passed < 0.2:
                offset = int(5 * (1 - time_passed / 0.2))
                cv2.rectangle(img, (x1 + offset, y1 + offset), (x2 + offset, y2 + offset), (180, 180, 180), -1)
                cv2.line(img, (x1 + offset, y1 + offset), (x2 + offset, y1 + offset), (100, 100, 100), 4)
                cv2.line(img, (x1 + offset, y1 + offset), (x1 + offset, y2 + offset), (100, 100, 100), 4)
                cv2.line(img, (x1 + offset, y2 + offset), (x2 + offset, y2 + offset), (220, 220, 220), 4)
                cv2.line(img, (x2 + offset, y2 + offset), (x2 + offset, y1 + offset), (220, 220, 220), 4)
                cv2.putText(img, text="P1 vs CPU", org=(x1 + 10+offset, y1 + 70+offset), fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=4,
                            lineType=4, thickness=4, color=(0, 0, 0), )
            else:
                self.state = "page2"
        else:
            cv2.rectangle(img, pt1, pt2, (0, 0, 0), 8)
            cv2.rectangle(img, pt1, pt2, (200, 200, 200), -1)

            cv2.putText(img,text="P1 vs CPU",org=(x1 + 10, y1 + 70),fontFace=cv2.FONT_HERSHEY_PLAIN,fontScale=4,
                        lineType=4,thickness=4,color=(0, 0, 0),)
        cv2.imshow("tic-tac-toe", img)

    def page2(self):
        img = np.ones((self.height, self.width, 3), dtype=np.uint8) * 255
        cv2.putText(img,text="choose the chess",org=(int(0.1 * self.width), int(0.15 * self.height)),
                    fontFace=cv2.FONT_HERSHEY_PLAIN,fontScale=4,lineType=4,thickness=4,color=(0, 0, 0),)
        cv2.putText(img, text="you like", org=(int(0.1 * self.width)+150, int(0.15 * self.height+50)),
                    fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=4, lineType=4, thickness=4, color=(0, 0, 0), )
        current_time = time.time()
        # O-chess
        x1, y1 = 100, 300
        pt1 = (x1, y1)
        x2, y2 = 350, 550
        pt2 = (x2, y2)
        center_x, center_y = int((x1 + x2) / 2), int((y1 + y2) / 2)
        center_pt = (center_x, center_y)
        radius = int((x2 - x1) / 2) - 20
        if self.press == "O":
            time_passed = current_time - self.press_time
            if time_passed < 0.2:
                offset = int(5 * (1 - time_passed / 0.2))
                cv2.rectangle(img, (x1 + offset, y1 + offset), (x2 + offset, y2 + offset), (180, 180, 180), -1)
                cv2.line(img, (x1 + offset, y1 + offset), (x2 + offset, y1 + offset), (100, 100, 100), 4)
                cv2.line(img, (x1 + offset, y1 + offset), (x1 + offset, y2 + offset), (100, 100, 100), 4)
                cv2.line(img, (x1 + offset, y2 + offset), (x2 + offset, y2 + offset), (220, 220, 220), 4)
                cv2.line(img, (x2 + offset, y2 + offset), (x2 + offset, y1 + offset), (220, 220, 220), 4)
                cv2.circle(img, (center_x+2*offset,center_y+2*offset), radius, (0, 0, 255), 8)
            else:
                self.state = "page3"

        else:
            cv2.rectangle(img, pt1, pt2, (0, 0, 0), 8)
            cv2.rectangle(img, pt2, pt1, (200, 200, 200), -1)
            cv2.circle(img, center_pt, radius, (0, 0, 255), 8)
        #X-chess
        x1 = x1 + 350
        pt1 = (x1, y1)
        x2 = x2 + 350
        pt2 = (x2, y2)
        if self.press == "X":
            time_passed = current_time - self.press_time
            if time_passed < 0.2:
                offset = int(5 * (1 - time_passed / 0.2))
                cv2.rectangle(img, (x1 + offset, y1 + offset), (x2 + offset, y2 + offset), (180, 180, 180), -1)
                cv2.line(img, (x1 + offset, y1 + offset), (x2 + offset, y1 + offset), (100, 100, 100), 4)
                cv2.line(img, (x1 + offset, y1 + offset), (x1 + offset, y2 + offset), (100, 100, 100), 4)
                cv2.line(img, (x1 + offset, y2 + offset), (x2 + offset, y2 + offset), (220, 220, 220), 4)
                cv2.line(img, (x2 + offset, y2 + offset), (x2 + offset, y1 + offset), (220, 220, 220), 4)

                cv2.line(img, (x1 + 20+offset, y1 + 20+offset), (x2 - 20+offset, y2 - 20+offset), (255, 0, 0), 8)
                cv2.line(img, (x2 - 20+offset, y1 + 20+offset), (x1 + 20+offset, y2 - 20+offset), (255, 0, 0), 8)
            else:
                self.state = "page3"
        else:
            cv2.rectangle(img, pt1, pt2, (0, 0, 0), 8)
            cv2.rectangle(img, pt2, pt1, (200, 200, 200), -1)
            cv2.line(img, (x1 + 20, y1 + 20), (x2 - 20, y2 - 20), (255, 0, 0), 8)
            cv2.line(img, (x2 - 20, y1 + 20), (x1 + 20, y2 - 20), (255, 0, 0), 8)
        cv2.imshow("tic-tac-toe", img)

    def page3(self):
        result = self.check_win()
        img = np.ones((self.height, self.width, 3), dtype=np.uint8) * 255
        # 绘制棋盘
        block_x1, block_x1_new = 100, 100
        block_y1, block_y1_new = 100, 100
        block_x2, block_x2_new = 300, 300
        block_y2, block_y2_new = 300, 300


        for i in range(3):
            for j in range(3):
                cv2.rectangle(img, (block_x1_new, block_y1_new), (block_x2_new, block_y2_new), (0, 0, 0), 8)
                if self.board[i][j] == 0:
                    center_x = int((block_x1_new + block_x2_new) / 2)
                    center_y = int((block_y1_new + block_y2_new) / 2)
                    radius = int((block_x2_new - block_x1_new) / 2) - 15
                    cv2.circle(img, (center_x, center_y), radius, (0, 0, 255), 8)
                elif self.board[i][j] == 1:
                    pt1 = (block_x1_new + 15, block_y1_new + 15)
                    pt2 = (block_x2_new - 15, block_y2_new - 15)
                    cv2.line(img, pt1, pt2, (255, 0, 0), 8)
                    pt1 = (block_x2_new - 15, block_y1_new + 15)
                    pt2 = (block_x1_new + 15, block_y2_new - 15)
                    cv2.line(img, pt1, pt2, (255, 0, 0), 8)
                block_x1_new = block_x1_new + 200
                block_x2_new = block_x2_new + 200
            block_x1_new = block_x1
            block_x2_new = block_x2
            block_y1_new = block_y1_new + 200
            block_y2_new = block_y2_new + 200
        if self.mode == 0:
            if self.current_player == 0:
                cv2.putText(img,"P1 <-----",(20,80),cv2.FONT_HERSHEY_PLAIN,fontScale=4,
                            lineType=4,thickness=4,color=(0,0,0),)
            elif self.current_player == 1:
                cv2.putText(img, "-----> P2", (400, 80), cv2.FONT_HERSHEY_PLAIN, fontScale=4,
                            lineType=4, thickness=4, color=(0, 0, 0), )
        else:
            if self.current_player == 0:
                cv2.putText(img,"P1 <-----",(20,80),cv2.FONT_HERSHEY_PLAIN,fontScale=4,
                            lineType=4,thickness=4,color=(0,0,0),)
            elif self.current_player == 1:
                cv2.putText(img, "-----> CPU", (350, 80), cv2.FONT_HERSHEY_PLAIN, fontScale=4,
                            lineType=4, thickness=4, color=(0, 0, 0), )

        current_time = time.time()
        #home
        x1,y1 = 20,720
        x2,y2 = 320,780
        offset_x = 65
        offset_y = 10
        if self.press == "home":
            time_passed = current_time - self.press_time
            if time_passed < 0.2:
                offset = int(5 * (1 - time_passed / 0.2))
                cv2.rectangle(img, (x1 + offset, y1 + offset), (x2 + offset, y2 + offset), (180, 180, 180), -1)
                cv2.line(img, (x1 + offset, y1 + offset), (x2 + offset, y1 + offset), (100, 100, 100), 4)
                cv2.line(img, (x1 + offset, y1 + offset), (x1 + offset, y2 + offset), (100, 100, 100), 4)
                cv2.line(img, (x1 + offset, y2 + offset), (x2 + offset, y2 + offset), (220, 220, 220), 4)
                cv2.line(img, (x2 + offset, y2 + offset), (x2 + offset, y1 + offset), (220, 220, 220), 4)
                cv2.putText(img, "home", (x1 + offset_x + offset, y2 - offset_y + offset), cv2.FONT_HERSHEY_PLAIN, fontScale=4,
                            lineType=4, thickness=4, color=(0, 0, 0))
            else:
                self.refresh()
        else:
            cv2.rectangle(img,(x1,y1),(x2,y2),(0,0,0),8)
            cv2.rectangle(img,(x1,y1),(x2,y2),(200,200,200),-1)
            cv2.putText(img,"home",(x1+offset_x,y2-offset_y),cv2.FONT_HERSHEY_PLAIN,fontScale=4,
                        lineType=4,thickness=4,color=(0,0,0))
        #undo
        x1, y1 = 480, 720
        x2, y2 = 780, 780
        offset_x = 65
        offset_y = 10
        if len(self.move_history)>0 and not self.game_over:
            if self.press == "undo":
                time_passed = current_time - self.press_time
                if time_passed < 0.2:
                    offset = int(5 * (1 - time_passed / 0.2))
                    cv2.rectangle(img, (x1 + offset, y1 + offset), (x2 + offset, y2 + offset), (180, 180, 180), -1)
                    cv2.line(img, (x1 + offset, y1 + offset), (x2 + offset, y1 + offset), (100, 100, 100), 4)
                    cv2.line(img, (x1 + offset, y1 + offset), (x1 + offset, y2 + offset), (100, 100, 100), 4)
                    cv2.line(img, (x1 + offset, y2 + offset), (x2 + offset, y2 + offset), (220, 220, 220), 4)
                    cv2.line(img, (x2 + offset, y2 + offset), (x2 + offset, y1 + offset), (220, 220, 220), 4)
                    cv2.putText(img, "undo", (x1 + offset_x+offset, y2 - offset_y+offset), cv2.FONT_HERSHEY_PLAIN, fontScale=4,
                                lineType=4, thickness=4, color=(0, 0, 0))
                else:
                    self.undo()
                    self.press = 0
            else:
                cv2.rectangle(img,(x1,y1),(x2, y2),(0,0,0),8)
                cv2.rectangle(img, (x1,y1), (x2, y2), (200, 200, 200), -1)
                cv2.putText(img, "undo", (x1 + offset_x, y2 - offset_y), cv2.FONT_HERSHEY_PLAIN, fontScale=4,
                            lineType=4, thickness=4, color=(0, 0, 0))
        else:#无法悔棋时设置为深色
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 0), 8)
            cv2.rectangle(img, (x1, y1), (x2, y2), (100, 100, 100), -1)
            cv2.putText(img, "undo", (x1 + offset_x, y2 - offset_y), cv2.FONT_HERSHEY_PLAIN, fontScale=4,
                        lineType=4, thickness=4, color=(0, 0, 0))

        #结算页面
        if self.game_over:
            self.winner = result
            cv2.rectangle(img,(100,100),(700,700),(220,220,220),-1)
            cv2.rectangle(img,(0,0),(800,90),(255,255,255),-1)
            if self.winner == 0:
                cv2.putText(img,"DRAW!",(200,400),cv2.FONT_HERSHEY_PLAIN,fontScale=8,
                            color=(0,0,0),lineType=4,thickness=4)
            else:
                if self.mode == 0:#2p对战模式
                    cv2.putText(img,f"P{self.winner}",(300,300),cv2.FONT_HERSHEY_PLAIN,fontScale=8,
                            color=(0,0,0),thickness=3)
                else:#人机对战模式
                    if self.winner == 1:
                        cv2.putText(img, "P1", (300, 300), cv2.FONT_HERSHEY_PLAIN, fontScale=8,
                                    color=(0, 0, 0), thickness=3)
                    elif self.winner == 2:
                        cv2.putText(img, "CPU", (300, 300), cv2.FONT_HERSHEY_PLAIN, fontScale=8,
                                    color=(0, 0, 0), thickness=3)
                cv2.putText(img,"WINNER!",(180,450),cv2.FONT_HERSHEY_PLAIN,fontScale=8,
                            color=(0,0,0),thickness=3)
            if self.press == "replay":
                time_passed = current_time - self.press_time
                if time_passed < 0.2:
                    offset = int(5 * (1 - time_passed / 0.2))
                    cv2.rectangle(img, (200 + offset, 550 + offset), (600 + offset, 650 + offset), (180, 180, 180), -1)
                    cv2.line(img, (200 + offset, 550 + offset), (600 + offset, 550 + offset), (100, 100, 100), 4)
                    cv2.line(img, (200 + offset, 550 + offset), (200 + offset, 650 + offset), (100, 100, 100), 4)
                    cv2.line(img, (200 + offset, 650 + offset), (600 + offset, 650 + offset), (220, 220, 220), 4)
                    cv2.line(img, (600 + offset, 650 + offset), (600 + offset, 550 + offset), (220, 220, 220), 4)
                    cv2.putText(img, "replay", (280+offset, 620+offset), cv2.FONT_HERSHEY_PLAIN, fontScale=4,
                                lineType=4, thickness=4, color=(0, 0, 0))
                else:
                    self.page3_init()
                    self.press = 0

            else:
                cv2.rectangle(img,(200,550),(600,650),(200,200,200),-1)
                cv2.rectangle(img,(200,550),(600,650),(0,0,0),4)
                cv2.putText(img,"replay",(280,620),cv2.FONT_HERSHEY_PLAIN,fontScale=4,
                            color=(0,0,0),lineType=4,thickness=4)
        cv2.imshow("tic-tac-toe", img)

    def mouse_callback(self,event,x,y,flags,param):
        #print(x,y)
        if event == cv2.EVENT_LBUTTONDOWN:
            self.click_process(x,y)
    def click_process(self,x,y):
        if self.state == "page1":
            if 200<=x<=580 and 250<=y<=350:
                self.press = "p1vsp2"
                self.press_time = time.time()
                self.mode = 0
            elif 200<=x<=580 and 500<=y<=600:
                self.press = "p1vsCpu"
                self.press_time = time.time()
                self.mode = 1
        elif self.state == "page2":
            if 100<=x<=350 and 300<=y<=550:
                self.press = "O"
                self.press_time = time.time()
                self.chess = 0
            elif 450<=x<=700 and 300<=y<=550:
                self.press = "X"
                self.press_time = time.time()
                self.chess = 1
        elif self.state == "page3":
            if 20<=x<=320 and 720<=y<=780:#home
                self.press = "home"
                self.press_time = time.time()
            elif 480<=x<=780 and 720<=y<=780:#undo
                if len(self.move_history)>0 and not self.game_over:
                    #self.undo()
                    self.press = "undo"
                    self.press_time = time.time()
            elif 100<=x<=700 and 100<=y<=700:
                row = (y-100)//200 #row 行,注意是y变大row才变大
                col = (x-100)//200 #col 列，注意是x变大col才变大
                if 0<=row<=2 and 0<=col<=2:
                    self.move_chess(row,col)
                    if self.mode == 1:
                        # self.page3()
                        # cv2.waitKey(1)
                        # time.sleep(0.5)
                        self.ai_move()
            if self.game_over:
                if 200<=x<=600 and 550<=y<=650:#replay
                    self.press = "replay"
                    self.press_time = time.time()
                    # self.page3_init()
                    # self.page3()

    def run(self):
        """运行游戏主循环"""
        cv2.setMouseCallback("tic-tac-toe",self.mouse_callback)

        while True:

            if self.state == "page1":
                self.page1()
            elif self.state == "page2":
                self.page2()
            elif self.state == "page3":
                self.page3()

            key = cv2.waitKey(1) & 0xFF
            if key == 27:  # ESC键退出
                break
            elif key == ord('q'):  # Q键退出
                break


        cv2.destroyAllWindows()

# 运行游戏
if __name__ == "__main__":
    game = TicTacToe()
    game.run()