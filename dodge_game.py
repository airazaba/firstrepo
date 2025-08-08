#!/usr/bin/env python3
"""Dodge the falling blocks in this modern 2D Pygame experience."""

import os
import random
import argparse
import pygame


def main() -> None:
    """Run the dodge game."""
    parser = argparse.ArgumentParser(description="Dodge the blocks in this modern 2D game.")
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run the game without a visible window for automated tests.",
    )
    args = parser.parse_args()

    if args.headless:
        os.environ["SDL_VIDEODRIVER"] = "dummy"

    pygame.init()
    width, height = 600, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Dodge!")

    clock = pygame.time.Clock()
    player = pygame.Rect(width // 2 - 25, height - 60, 50, 50)
    enemy_size = 50
    enemies: list[pygame.Rect] = []
    enemy_spawn_time = 0
    spawn_delay = 1000  # milliseconds

    running = True
    score = 0
    start_ticks = pygame.time.get_ticks()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.left > 0:
            player.move_ip(-5, 0)
        if keys[pygame.K_RIGHT] and player.right < width:
            player.move_ip(5, 0)

        current_time = pygame.time.get_ticks()
        if current_time - enemy_spawn_time > spawn_delay:
            enemy_spawn_time = current_time
            enemy = pygame.Rect(
                random.randint(0, width - enemy_size), -enemy_size, enemy_size, enemy_size
            )
            enemies.append(enemy)
        speed = 5 + score // 5

        for enemy in enemies[:]:
            enemy.move_ip(0, speed)
            if enemy.top > height:
                enemies.remove(enemy)
                score += 1

        for enemy in enemies:
            if player.colliderect(enemy):
                running = False

        screen.fill((30, 30, 30))
        pygame.draw.rect(screen, (0, 200, 255), player)
        for enemy in enemies:
            pygame.draw.rect(screen, (200, 30, 30), enemy)

        font = pygame.font.Font(None, 36)
        score_surf = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_surf, (10, 10))

        pygame.display.flip()
        clock.tick(60)

        if args.headless and current_time - start_ticks > 3000:
            running = False

    if args.headless:
        print(f"Final score: {score}")

    pygame.quit()


if __name__ == "__main__":
    main()
