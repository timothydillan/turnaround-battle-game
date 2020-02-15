import pygame as pg

class Button(object):
    '''
    Example can found in run_button.py.py
    
    '''
    def __init__(self,rect,command,**kwargs):
        '''
        Optional kwargs and their defaults:
            "color"             : pg.Color('red'),
            "text"              : None,
            "font"              : None, #pg.font.Font(None,16),
            "call_on_release"   : True,
            "hover_color"       : None,
            "clicked_color"     : None,
            "font_color"        : pg.Color("white"),
            "hover_font_color"  : None,
            "clicked_font_color": None,
            "click_sound"       : None,
            "hover_sound"       : None,
            'border_color'      : pg.Color('black'),
            'border_hover_color': pg.Color('yellow'),
            'disabled'          : False,
            'disabled_color'     : pg.Color('grey'),
            'radius'            : 3,
            
        Values:
            self.rect = pg.Rect(rect)
            self.command = command
            self.clicked = False
            self.hovered = False
            self.hover_text = None
            self.clicked_text = None
        '''
        self.rect = pg.Rect(rect)
        self.command = command
        self.clicked = False
        self.hovered = False
        self.hover_text = None
        self.clicked_text = None
        self.process_kwargs(kwargs)
        self.render_text()

    def process_kwargs(self,kwargs):
        settings = {
            "color"             : pg.Color('red'),
            "text"              : None,
            "font"              : None, #pg.font.Font(None,16),
            "call_on_release"   : True,
            "hover_color"       : None,
            "clicked_color"     : None,
            "font_color"        : pg.Color("white"),
            "hover_font_color"  : None,
            "clicked_font_color": None,
            "click_sound"       : None,
            "hover_sound"       : None,
            'border_color'      : pg.Color('black'),
            'border_hover_color': pg.Color('yellow'),
            'disabled'          : False,
            'disabled_color'     : pg.Color('grey'),
            'radius'            : 3,
        }
        for kwarg in kwargs:
            if kwarg in settings:
                settings[kwarg] = kwargs[kwarg]
            else:
                raise AttributeError("{} has no keyword: {}".format(self.__class__.__name__, kwarg))
        self.__dict__.update(settings)

    def render_text(self):
        """Pre render the button text."""
        if self.text:
            if self.hover_font_color:
                color = self.hover_font_color
                self.hover_text = self.font.render(self.text,True,color)
            if self.clicked_font_color:
                color = self.clicked_font_color
                self.clicked_text = self.font.render(self.text,True,color)
            self.text = self.font.render(self.text,True,self.font_color)

    def get_event(self,event):
        ''' Call this on your event loop
        
            for event in pg.event.get():
                Button.get_event(event)
        '''
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            self.on_click(event)
        elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
            self.on_release(event)

    def on_click(self,event):
        if self.rect.collidepoint(event.pos):
            self.clicked = True
            if not self.call_on_release:
                self.function()


    def on_release(self,event):
        if self.clicked and self.call_on_release:
            #if user is still within button rect upon mouse release
            if self.rect.collidepoint(pg.mouse.get_pos()):
                self.command()
        self.clicked = False

    def check_hover(self):
        if self.rect.collidepoint(pg.mouse.get_pos()):
            if not self.hovered:
                self.hovered = True
                if self.hover_sound:
                    self.hover_sound.play()
        else:
            self.hovered = False

    def draw(self,surface):
        '''
        Call once on your main game loop
        '''
        color = self.color
        text = self.text
        border = self.border_color
        self.check_hover()
        if not self.disabled:
            if self.clicked and self.clicked_color:
                color = self.clicked_color
                if self.clicked_font_color:
                    text = self.clicked_text
            elif self.hovered and self.hover_color:
                color = self.hover_color
                if self.hover_font_color:
                    text = self.hover_text
            if self.hovered and not self.clicked:
                border = self.border_hover_color
        else:
            color = self.disabled_color
        
        #if not self.rounded:
        #    surface.fill(border,self.rect)
        #    surface.fill(color,self.rect.inflate(-4,-4))
        #else:
        if self.radius:
            rad = self.radius
        else:
            rad = 0
        self.round_rect(surface, self.rect , border, rad, 1, color)
        if self.text:
            text_rect = text.get_rect(center=self.rect.center)
            surface.blit(text,text_rect)
            
            
    def round_rect(self, surface, rect, color, rad=20, border=0, inside=(0,0,0,0)):
        rect = pg.Rect(rect)
        zeroed_rect = rect.copy()
        zeroed_rect.topleft = 0,0
        image = pg.Surface(rect.size).convert_alpha()
        image.fill((0,0,0,0))
        self._render_region(image, zeroed_rect, color, rad)
        if border:
            zeroed_rect.inflate_ip(-2*border, -2*border)
            self._render_region(image, zeroed_rect, inside, rad)
        surface.blit(image, rect)


    def _render_region(self, image, rect, color, rad):
        corners = rect.inflate(-2*rad, -2*rad)
        for attribute in ("topleft", "topright", "bottomleft", "bottomright"):
            pg.draw.circle(image, color, getattr(corners,attribute), rad)
        image.fill(color, rect.inflate(-2*rad,0))
        image.fill(color, rect.inflate(0,-2*rad))
        
    def update(self):
        #for completeness
        pass
