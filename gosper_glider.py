#Gosper Glider Gun coordinates
def gosper_glider_builder():
    
    figure_a = [(100, 500), (120, 500), (100, 520), (120, 520)]
    
    figure_b = [(780, 480), (780, 460), (800, 480), (800, 460)]

    figure_c = [(300, 500), (300, 520), (300, 540), (320, 480), (320, 560),
                (340, 460), (340, 580), (360, 460), (360, 580), (380, 520),
                (400, 480), (400, 560), (420, 500), (420, 520), (420, 540),
                (440, 520)]

    figure_d = [(500, 500), (500, 480), [500, 460], (520, 500), (520, 480), (520, 460),
                (540, 440), (540, 520), (580, 420), (580, 440), (580, 520), (580, 540)]

    fig_list = figure_a + figure_b + figure_c + figure_d

    return fig_list
