import pygame  # 게임 개발을 위한 Pygame 라이브러리 가져오기
import random  # 랜덤 숫자를 생성하기 위한 라이브러리
import sys  # 시스템 종료 등을 위한 라이브러리

# Pygame 초기화
pygame.init()

# 화면 크기 설정
WIDTH, HEIGHT = 800, 600  # 화면 너비와 높이를 픽셀 단위로 설정
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # 화면 생성
pygame.display.set_caption("우주선 vs 혜성")  # 게임 창 제목 설정

# 색상 정의 (RGB 값으로 설정)
WHITE = (255, 255, 255)  # 흰색
BLACK = (0, 0, 0)  # 검은색
RED = (255, 0, 0)  # 빨간색

# 폰트 초기화
font = pygame.font.SysFont("Arial", 24)  # Arial 폰트, 크기 24로 설정

# 우주선 클래스 정의
class Spaceship:
    def __init__(self):
        self.image = pygame.Surface((50, 30))  # 우주선 크기 설정 (50x30 픽셀)
        self.image.fill(WHITE)  # 우주선 색상을 흰색으로 설정
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT - 50))  # 우주선 위치를 화면 아래쪽 중앙으로 설정
        self.speed = 5  # 우주선 이동 속도

    def move(self, keys):
        # 키 입력에 따라 우주선을 왼쪽 또는 오른쪽으로 이동
        if keys[pygame.K_LEFT] and self.rect.left > 0:  # 왼쪽 화살표 키를 누르고 화면 밖으로 나가지 않으면
            self.rect.x -= self.speed  # 왼쪽으로 이동
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:  # 오른쪽 화살표 키를 누르고 화면 밖으로 나가지 않으면
            self.rect.x += self.speed  # 오른쪽으로 이동

    def draw(self, screen):
        # 우주선을 화면에 그리기
        screen.blit(self.image, self.rect)

# 혜성 클래스 정의
class Comet:
    def __init__(self):
        self.image = pygame.Surface((30, 30))  # 혜성 크기 설정 (30x30 픽셀)
        self.color = RED  # 혜성 색상을 빨간색으로 설정
        self.image.fill(self.color)  # 혜성 색상 적용
        self.rect = self.image.get_rect(center=(random.randint(0, WIDTH), 0))  # 혜성 위치를 화면 위쪽에서 랜덤으로 설정
        self.speed = random.randint(3, 7)  # 혜성 이동 속도를 랜덤으로 설정

    def move(self):
        self.rect.y += self.speed  # 혜성을 아래로 이동

    def draw(self, screen):
        # 혜성을 화면에 그리기
        screen.blit(self.image, self.rect)

# 게임 오버 화면
def game_over_screen(score, high_score):
    if score > high_score:
        high_score = score  # 하이 스코어 갱신
    while True:
        screen.fill(BLACK)  # 화면을 검은색으로 채우기
        # 게임 오버 메시지와 점수 표시
        game_over_text = font.render("Game Over!", True, RED)
        final_score_text = font.render(f"Final Score: {score}", True, WHITE)
        high_score_text = font.render(f"High Score: {high_score}", True, WHITE)
        restart_text = font.render("Press R to Restart or Q to Quit", True, WHITE)

        # 화면 중앙에 텍스트 표시
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 90))
        screen.blit(final_score_text, (WIDTH // 2 - final_score_text.get_width() // 2, HEIGHT // 2 - 40))
        screen.blit(high_score_text, (WIDTH // 2 - high_score_text.get_width() // 2, HEIGHT // 2 + 10))
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 60))

        pygame.display.flip()  # 화면 업데이트

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # 창 닫기 버튼을 누르면 게임 종료
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # R 키를 누르면 게임 재시작
                    return high_score, True
                if event.key == pygame.K_q:  # Q 키를 누르면 게임 종료
                    pygame.quit()
                    sys.exit()

# 게임 루프
def main(high_score=0):
    clock = pygame.time.Clock()  # FPS를 제어하기 위한 시계
    spaceship = Spaceship()  # 우주선 객체 생성
    comets = [Comet() for _ in range(5)]  # 초기 혜성 5개 생성
    running = True
    score = 0  # 점수 초기화
    score_timer = 0  # 점수 증가 타이머
    difficulty_timer = 0  # 난이도 조정 타이머
    comet_spawn_timer = 0  # 혜성 추가 타이머

    while running:
        screen.fill(BLACK)  # 화면을 검은색으로 채우기
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # 창 닫기 버튼을 누르면 게임 종료
                running = False

        keys = pygame.key.get_pressed()  # 키 입력 상태 확인
        spaceship.move(keys)  # 우주선 이동

        # 혜성 이동 및 충돌 처리
        for comet in comets[:]:  # 리스트 복사본을 사용하여 안전하게 제거
            comet.move()
            if comet.rect.top > HEIGHT:  # 화면 아래로 나간 혜성 제거
                comets.remove(comet)
                comets.append(Comet())  # 새로운 혜성 추가
            if comet.rect.colliderect(spaceship.rect):  # 혜성과 우주선 충돌 체크
                running = False  # 게임 종료

        # 점수 업데이트 (0.5초마다 증가)
        score_timer += clock.get_time() / 1000  # 밀리초를 초로 변환
        if score_timer >= 0.5:  # 0.5초마다 실행
            score += 1
            score_timer = 0

        # 난이도 증가 (1초마다 혜성 속도 증가)
        difficulty_timer += clock.get_time() / 1000
        if difficulty_timer >= 1:
            for comet in comets:
                comet.speed += 1  # 혜성 속도 증가
            difficulty_timer = 0

        # 혜성 추가 (5초마다 새로운 혜성 추가)
        comet_spawn_timer += clock.get_time() / 1000
        if comet_spawn_timer >= 5:
            comets.append(Comet())  # 새로운 혜성 추가
            comet_spawn_timer = 0

        # 점수 및 하이 스코어 표시
        score_text = font.render(f"Score: {score}", True, WHITE)
        high_score_text = font.render(f"High Score: {high_score}", True, WHITE)
        screen.blit(score_text, (10, 40))
        screen.blit(high_score_text, (10, 10))

        # 우주선 및 혜성 그리기
        spaceship.draw(screen)
        for comet in comets:
            comet.draw(screen)

        pygame.display.flip()  # 화면 업데이트
        clock.tick(60)  # 초당 60프레임으로 실행

    # 게임 오버 화면 호출
    high_score, restart = game_over_screen(score, high_score)
    if restart:
        main(high_score)  # 게임 재시작

if __name__ == "__main__":
    main()  # 게임 실행
