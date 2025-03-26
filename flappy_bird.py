import pygame  # 게임 개발을 위한 Pygame 라이브러리 가져오기
import random  # 랜덤 숫자를 생성하기 위한 라이브러리
import sys  # 시스템 종료 등을 위한 라이브러리

# Pygame 초기화
pygame.init()

# 화면 크기 설정
WIDTH, HEIGHT = 400, 600  # 화면 너비와 높이를 픽셀 단위로 설정
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # 화면 생성
pygame.display.set_caption("Flappy Bird")  # 게임 창 제목 설정

# 색상 정의 (RGB 값으로 설정)
WHITE = (255, 255, 255)  # 흰색
BLACK = (0, 0, 0)  # 검은색
BLUE = (0, 0, 255)  # 파란색
GREEN = (0, 255, 0)  # 초록색
RED = (255, 0, 0)  # 빨간색

# 폰트 초기화
font = pygame.font.SysFont("Arial", 24)  # Arial 폰트, 크기 24로 설정

# 배경 이미지 로드
try:
    background_image = pygame.image.load("background.png")  # 배경 이미지 파일 로드
    background_image = pygame.transform.scale(background_image, (WIDTH * 2, HEIGHT))  # 배경 이미지 크기 조정
except pygame.error:
    background_image = None  # 이미지 파일이 없으면 None으로 설정

# 새 클래스 정의
class Bird:
    def __init__(self):
        self.x = 100  # 새의 초기 x 좌표
        self.y = HEIGHT // 2  # 새의 초기 y 좌표 (화면 중앙)
        self.radius = 12  # 새의 반지름 (충돌 판정을 위한 원의 크기)
        self.gravity = 0.5  # 중력 효과 (새가 아래로 떨어지는 속도)
        self.lift = -10  # 새가 날아오를 때의 속도
        self.velocity = 0  # 새의 현재 속도
        try:
            self.image = pygame.image.load("bird.png")  # 새 이미지 로드
            self.image = pygame.transform.scale(self.image, (40, 40))  # 새 이미지 크기 조정
        except pygame.error:
            self.image = None  # 이미지 파일이 없으면 None으로 설정

    def flap(self):
        self.velocity = self.lift  # 스페이스바를 누르면 위로 날아오름

    def move(self):
        self.velocity += self.gravity  # 중력 효과로 속도 증가
        self.y += self.velocity  # 속도에 따라 y 좌표 변경

    def draw(self, screen):
        if self.image:
            # 새 이미지를 화면에 그리기
            screen.blit(self.image, (self.x - self.image.get_width() // 2, self.y - self.image.get_height() // 2))
        else:
            # 이미지가 없으면 파란색 원으로 새를 그리기
            pygame.draw.circle(screen, BLUE, (self.x, int(self.y)), self.radius)

    def check_collision(self):
        # 새가 화면 위나 아래로 나가면 충돌로 간주
        if self.y - self.radius < 0 or self.y + self.radius > HEIGHT:
            return True
        return False

# 파이프 클래스 정의
class Pipe:
    image_top = pygame.image.load("pipe_top.png")  # 위쪽 파이프 이미지 로드
    image_bottom = pygame.image.load("pipe_bottom.png")  # 아래쪽 파이프 이미지 로드

    def __init__(self, speed=3):
        self.x = WIDTH  # 파이프의 초기 x 좌표 (화면 오른쪽 끝)
        self.width = 50  # 파이프의 너비
        self.gap = 150  # 위쪽 파이프와 아래쪽 파이프 사이의 간격
        self.top_height = random.randint(50, HEIGHT - self.gap - 50)  # 위쪽 파이프의 높이
        self.bottom_height = HEIGHT - self.top_height - self.gap  # 아래쪽 파이프의 높이
        self.speed = speed  # 파이프가 왼쪽으로 이동하는 속도

        # 파이프 이미지를 크기에 맞게 조정
        self.image_top_scaled = pygame.transform.scale(Pipe.image_top, (self.width, self.top_height))
        self.image_bottom_scaled = pygame.transform.scale(Pipe.image_bottom, (self.width, self.bottom_height))

        # 파이프가 위아래로 움직이는지 여부 (10% 확률)
        self.is_moving = random.random() < 0.1
        self.moving_direction = 1  # 1이면 아래로, -1이면 위로 이동
        self.moving_speed = 2  # 위아래 이동 속도

    def move(self):
        self.x -= self.speed  # 파이프를 왼쪽으로 이동

        # 파이프 위아래 움직임 처리
        if self.is_moving:
            if self.top_height <= 50 or self.bottom_height <= 50:
                self.moving_direction *= -1  # 방향 반전
            self.top_height += self.moving_direction * self.moving_speed
            self.bottom_height = HEIGHT - self.top_height - self.gap

            # 파이프 이미지를 크기에 맞게 다시 조정
            self.image_top_scaled = pygame.transform.scale(Pipe.image_top, (self.width, self.top_height))
            self.image_bottom_scaled = pygame.transform.scale(Pipe.image_bottom, (self.width, self.bottom_height))

    def draw(self, screen):
        # 위쪽 파이프 그리기
        screen.blit(self.image_top_scaled, (self.x, 0))
        # 아래쪽 파이프 그리기
        screen.blit(self.image_bottom_scaled, (self.x, HEIGHT - self.bottom_height))

    def check_collision(self, bird):
        # 새와 파이프의 충돌 체크
        bird_rect = pygame.Rect(bird.x - bird.radius, bird.y - bird.radius, bird.radius * 2, bird.radius * 2)
        pipe_top_rect = pygame.Rect(self.x, 0, self.width, self.top_height)
        pipe_bottom_rect = pygame.Rect(self.x, HEIGHT - self.bottom_height, self.width, self.bottom_height)
        if bird_rect.colliderect(pipe_top_rect) or bird_rect.colliderect(pipe_bottom_rect):
            return True
        return False

# 게임 시작 대기 화면
def wait_for_start():
    while True:
        # 배경 이미지 그리기
        if background_image:
            screen.blit(background_image, (0, 0))
        else:
            screen.fill(BLACK)  # 이미지가 없으면 검은색 배경

        # 투명도 60%의 검은색 오버레이
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(153)  # 255 * 0.6 = 153 (투명도 60%)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))

        # 시작 메시지 표시
        start_text = font.render("Press SPACE to Start", True, WHITE)
        screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2 - 20))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # 스페이스바를 누르면 시작
                    return

# 게임 종료 화면
def game_over_screen(score, high_score):
    if score > high_score:
        high_score = score  # 하이 스코어 갱신
    while True:
        screen.fill(BLACK)
        game_over_text = font.render("Game Over!", True, RED)
        final_score_text = font.render(f"Final Score: {score}", True, WHITE)
        high_score_text = font.render(f"High Score: {high_score}", True, WHITE)
        restart_text = font.render("Press R to Restart or Q to Quit", True, WHITE)

        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 90))
        screen.blit(final_score_text, (WIDTH // 2 - final_score_text.get_width() // 2, HEIGHT // 2 - 40))
        screen.blit(high_score_text, (WIDTH // 2 - high_score_text.get_width() // 2, HEIGHT // 2 + 10))
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 60))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
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
    bird = Bird()  # 새 객체 생성
    pipes = [Pipe()]  # 파이프 리스트 초기화
    running = True
    score = 0  # 점수 초기화
    speed = 3  # 초기 파이프 속도

    # 배경 스크롤 변수
    bg_x1 = 0
    bg_x2 = WIDTH * 2  # 배경 이미지 크기와 일치하도록 설정

    # 게임 시작 대기
    wait_for_start()

    while running:
        # 배경 스크롤
        bg_x1 -= speed  # 배경 스크롤 속도를 파이프 속도와 연동
        bg_x2 -= speed
        if bg_x1 + WIDTH * 2 <= 0:  # 배경 이미지 크기와 일치하도록 수정
            bg_x1 = bg_x2 + WIDTH * 2
        if bg_x2 + WIDTH * 2 <= 0:
            bg_x2 = bg_x1 + WIDTH * 2

        # 배경 이미지 그리기
        if background_image:
            screen.blit(background_image, (bg_x1, 0))
            screen.blit(background_image, (bg_x2, 0))
        else:
            screen.fill(BLACK)  # 이미지가 없으면 검은색 배경

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.flap()

        # 새 이동
        bird.move()

        # 파이프 이동 및 생성
        for pipe in pipes:
            pipe.move()
            if pipe.x + pipe.width < 0:  # 화면 밖으로 나간 파이프 제거
                pipes.remove(pipe)
                pipes.append(Pipe(speed))  # 새로운 파이프 추가
                score += 1  # 점수 증가

                # 점수가 5의 배수일 때 속도 증가
                if score % 5 == 0:
                    speed += 0.5  # 속도 증가량을 기존보다 더 크게 조정

        # 충돌 체크
        if bird.check_collision():
            running = False
        for pipe in pipes:
            if pipe.check_collision(bird):
                running = False

        # 그리기
        bird.draw(screen)
        for pipe in pipes:
            pipe.draw(screen)

        # 점수 및 하이 스코어 표시
        score_text = font.render(f"Score: {score}", True, WHITE)
        high_score_text = font.render(f"High Score: {high_score}", True, WHITE)
        screen.blit(score_text, (10, 40))
        screen.blit(high_score_text, (10, 10))

        pygame.display.flip()
        clock.tick(60)  # 초당 60프레임으로 실행

    # 게임 종료 화면 호출
    high_score, restart = game_over_screen(score, high_score)
    if restart:
        main(high_score)  # 게임 재시작

if __name__ == "__main__":
    main()  # 게임 실행
