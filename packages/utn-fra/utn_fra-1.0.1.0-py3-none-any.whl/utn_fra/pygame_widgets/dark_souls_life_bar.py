# Copyright (C) 2025 <UTN FRA>
#
# Author: Facundo Falcone <f.falcone@sistemas-utnfra.com.ar>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import pygame as pg

class DarkSoulsLifeBar(pg.sprite.Sprite):
    
    def __init__(self, screen: pg.Surface, current_healt: float, maximum_healt: float, health_bar_length, pos: tuple[int,int], health_speed: int=20, bar_type: str = 'vitality') -> None:
        super().__init__()
        self.base_colors = {
            "stamina": {
                "primary": pg.Color('yellow'),
                "secondary": pg.Color('gold'),
                "background": (125,125,0)
            },
            "mana": {
                "primary": pg.Color('cyan'),
                "secondary": pg.Color('lightblue'),
                "background": pg.Color('aliceblue')
            },
            "vitality": {
                "primary": pg.Color('green'),
                "secondary": pg.Color('yellow'),
                "background": pg.Color('red')
            },
        }
        self.background_empty_bar_color = (30,30,30)
        self.screen = screen
        self.pos = pos
        self.bar_type = self.base_colors.get(bar_type, 'vitality')
        self.image = pg.Surface((40,40))
        self.image.fill((240,240,240))
        self.rect = self.image.get_rect(center = (400,400))
        self.current_health = current_healt
        self.target_health = self.current_health + 100
        self.maximum_health = maximum_healt
        self.health_bar_length = health_bar_length
        self.health_ratio = self.maximum_health / self.health_bar_length
        self.health_change_speed = health_speed
        self.transition_width = 0
        self.transition_color = (255,0,0)
        
    def get_max_amount(self) -> int:
        return self.maximum_health
    
    def get_actual_amount(self) -> int:
        return self.target_health
    
    def set_damage(self, amount: int) -> None:
        if self.target_health > 0:
            self.target_health -= amount
        if self.target_health <= 0:
            self.target_health = 0
    
    def set_health(self, amount: int) -> None:
        if self.target_health < self.maximum_health:
            self.target_health += amount
        if self.target_health >= self.maximum_health:
            self.target_health = self.maximum_health
    
    def advanced_health(self) -> None:
        transition_width = 0
        transition_color = self.bar_type.get('primary')
        
        if self.current_health < self.target_health:
            self.current_health += self.health_change_speed
            transition_width = int((self.target_health- self.current_health)/self.health_ratio)
            transition_color = self.bar_type.get('secondary')
        
        elif self.current_health > self.target_health:
            self.current_health -= self.health_change_speed
            transition_width = int((self.target_health - self.current_health)/ self.health_ratio)
            transition_color = (255,0,0)
        
        health_bar_rect =  pg.Rect(self.pos[0], self.pos[1], self.current_health/self.health_ratio, 25)
        transition_bar_rect = pg.Rect(health_bar_rect.right, self.pos[1], transition_width, 25)
        
        pg.draw.rect(self.screen, self.bar_type.get('background'), (self.pos[0],self.pos[1], self.health_bar_length, 25))
        pg.draw.rect(self.screen, self.bar_type.get('primary'), health_bar_rect)
        pg.draw.rect(self.screen, transition_color, transition_bar_rect)
        pg.draw.rect(self.screen, (255,255,255), (self.pos[0],self.pos[1], self.health_bar_length, 25), 4)
        
        pg.draw.rect(self.screen, pg.Color('white'), (self.pos[0],self.pos[1], self.health_bar_length, 25), 4)
    
    def update_target_health(self, amount: int) -> None:
        if amount > self.target_health:
            total = amount - self.target_health
            self.set_health(total)
        elif amount < self.target_health:
            total = self.target_health - amount
            self.set_damage(total)
    
    def update(self, actual_health: int) -> None:
        self.update_target_health(actual_health)
    
    def draw(self) -> None:
        self.advanced_health()
