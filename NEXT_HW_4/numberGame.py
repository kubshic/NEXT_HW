# 숫자 맞추기 게임!

# 사용자가 1부터 100까지의 숫자 중 하나를 생각한다
# 컴퓨터는 1부터 100까지의 중간값을 제시한다
# 사용자는 컴퓨터가 제시한 숫자가 생각한 숫자보다 큰지, 작은지, 아니면 맞는지를 알려준다
# 컴퓨터는 사용자의 피드백에 따라 제시하는 숫자의 범위를 좁혀 나간다.
# 이 과정은 컴퓨터가 숫자를 맞출 때까지 반복된다.



low = 1
high = 101
import statistics
import random
number_range = list(range(low,high))
median = round(statistics.median(number_range))
input('1부터 100까지의 숫자 중 하나를 생각하세요. 숫자 맞추기 게임을 시작하려면 Enter를 누르세요.')
compare = input('당신이 생각한 숫자가 {}보다 큰가요? (예/아니요) (생각한 숫자가 {}이라면 정답이라고 적어주세요.)'.format(median, median))

while compare not in ['예', '아니요', '정답']:
    compare = input('다시 입력해 주세요. (예/아니요/정답)')
if compare == '정답':
        print('역시 그럴줄 알았어요!')
    
while compare in ['예', '아니요']:
    if compare == '예':
        low = median + 1
        hint = high - low
    elif compare == '아니요':
        high = median
        hint = high - low
    if hint < 4:
        break
    number_range = list(range(low,high))
    median = round(statistics.median(number_range))
    hint = high - low
    compare = input('당신이 생각한 숫자가 {}보다 큰가요? (예/아니요) (생각한 숫자가 {}이라면 정답이라고 적어주세요.)'.format(median, median))
new_low = low
new_list = list(range(new_low,high))
random_number= random.choice(new_list)
answer = input('당신이 생각한 숫자는 {}입니까? (예/아니요)'.format(random_number))
if answer == '아니요':
    for number in new_list:
        if number != random_number:
            print('정답은', number)
if answer == '예':
    print('역시 그럴줄 알았어요!')
            
            
    #while compare == '아니요':
    #    high = median
    #    number_range = list(range(low,high))
     #   median = round(statistics.median(number_range))
      #  compare = input('당신이 생각한 숫자가 {}보다 큰가요? (예/아니요) (생각한 숫자가 {}이라면 정답이라고 적어주세요.)'.format(median, median))
      #  hint = high - low
      #  if hint < 3:
       #     new_low = low + 1
      #      new_list = list(range(new_low,high))
       #     random_number= random.randrange(new_low,high)
       #     answer = input('당신이 생각한 숫자는 {}입니까? (예/아니요)'.format(random_number))
        #    if answer == '아니요':
        #        new_list.remove(random_number)
         #       print('정답은 {}'.format(new_list[0]))
         #   if answer == '예':
         #       print('역시 그럴줄 알았어요!')