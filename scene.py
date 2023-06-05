import manim
import numpy as np
from manim import *
import random
from scipy.stats import t


class BarChartExample(Scene):
    def construct(self):
        self.current_anim = 0
        self.prev_anim = 0
        # INTRO:

        # # DATA tables
        datatable1 = Table(
            [
                ["18"],
                ["29"],
                ["47"]
            ],
            row_labels=[Text("Cats"), Text("Dogs"), Text("Total")],
            col_labels=[Text("Sum of Siblings")],
            top_left_entry=Text('Group Names'),
            include_outer_lines=True

        )
        datatable2 = Table(
            [
                ['15', '1.2', '0.775', '0', '1', '1', '2', '3'],
                ['17', '1.529', '0.874', '0', '1', '1', '2', '4'],

            ],
            row_labels=[Text("Cat People # of Siblings"), Text("Cat People # of Siblings")],
            col_labels=[Text('n'), Text('mean'), Text('SD'), Text('min'), Text('Q1'), Text('med'), Text('Q3'),
                        Text('max')],
            top_left_entry=Text('Group Names'),
            include_outer_lines=True
        ).scale_to_fit_width(datatable1.width * 1.2)
        VGroup(datatable1, datatable2).arrange(DOWN, buff=0.05)
        # table 1 anims
        self.wait(3)
        self.play(Create(datatable1.shift(1.5 * DOWN)))
        self.wait(3)
        datatable1.add(datatable1.get_cell((2, 2), color=YELLOW))
        self.wait(3)
        datatable1.add(datatable1.get_cell((2, 2), color=WHITE))
        datatable1.add(datatable1.get_cell((3, 2), color=YELLOW))
        self.wait(3)
        datatable1.add(datatable1.get_cell((3, 2), color=WHITE))
        datatable1copy = datatable1.copy().scale(0.8).shift(1 * UP)
        self.play(FadeTransform(datatable1, datatable1copy))
        self.play(SpinInFromNothing(datatable2))
        # table 2 anims
        # means
        datatable2.add(
            datatable2.get_cell((2, 3), color=YELLOW),
            datatable2.get_cell((3, 3), color=YELLOW)
        )
        self.wait(2)
        datatable2.add(
            datatable2.get_cell((2, 3), color=WHITE),
            datatable2.get_cell((3, 3), color=WHITE)
        )
        self.wait()
        # SD's
        datatable2.add(datatable2.get_cell((1, 4), color=YELLOW))
        self.wait(1.5)
        # min's
        datatable2.add(datatable2.get_cell((1, 4), color=WHITE),
                       datatable2.get_cell((1, 5), color=YELLOW))
        self.wait(1.5)
        # max's
        datatable2.add(datatable2.get_cell((1, 5), color=WHITE),
                       datatable2.get_cell((1, 9), color=YELLOW))
        self.wait(1.5)
        # quarters
        datatable2.add(datatable2.get_cell((1, 9), color=WHITE),
                       datatable2.get_cell((1, 6), color=YELLOW),
                       datatable2.get_cell((1, 8), color=YELLOW))
        self.wait(2)
        #sample size (n)
        datatable2.add(datatable2.get_cell((1, 6), color=WHITE),
                       datatable2.get_cell((1, 8), color=WHITE),
                       datatable2.get_cell((2, 2), color=YELLOW),
                       datatable2.get_cell((3, 2), color=YELLOW),
                       )
        self.wait(3)
        datatable2.add(
                       datatable2.get_cell((2, 2), color=WHITE),
                       datatable2.get_cell((3, 2), color=WHITE),
                       )
        self.wait(5)
        self.play(ShrinkToCenter(datatable1copy), ShrinkToCenter(datatable2))

        # cat people chart
        catchart, cattitle, catxlabel, catylabel = self.create_graph(
            [2, 9, 3, 1, 0],
            ["one", "two", "three", "four", "five"],
            [0, 10, 1],
            "Cat People",
            "\\# of Siblings",
            "\\# of People",
        )
        self.play(FadeIn(cattitle, catxlabel, catylabel, run_time=1.5))
        self.play(GrowFromEdge(catchart, LEFT))
        self.wait(5)
        self.play(FadeOut(cattitle, catxlabel, catylabel))
        self.play(FadeOut(catchart))

        # dog people chart
        dogchart, dogtitle, dogxlabel, dogylabel = self.create_graph(
            [1, 8, 7, 0, 1],
            ["one", "two", "three", "four", "five"],
            [0, 10, 1],
            "Dog People",
            "\\# of Siblings",
            "\\# of People",
        )
        self.play(FadeIn(dogtitle, dogxlabel, dogylabel))
        self.play(FadeIn(dogchart))
        self.wait(5)

        # both chart animation
        self.play(FadeOut(dogtitle, dogxlabel, dogylabel))
        scale = 0.8
        todogchart = dogchart.copy().scale(scale).shift(2.5*RIGHT)
        tocatchart = catchart.copy().scale(scale).shift(2.5*LEFT)
        dogtitle = Text("Dog People").set_color(YELLOW).shift(3*UP).shift(2.5*RIGHT)
        cattitle = Text("Cat People").set_color(YELLOW).shift(3*UP).shift(2.5*LEFT)
        self.play(
            FadeTransform(dogchart, todogchart, stretch=True, dim_to_match=0),
            DrawBorderThenFill(tocatchart),
            FadeIn(cattitle, dogtitle)
        )
        self.wait(4)

        self.play(ShrinkToCenter(tocatchart), ShrinkToCenter(todogchart), ShrinkToCenter(cattitle), ShrinkToCenter(dogtitle))
        dualtitle = Text("Cat People").set_color(YELLOW).shift(3*UP)
        self.play(FadeIn(catchart, dualtitle))
        self.wait(3)
        self.play(FadeOut(dualtitle))
        dualtitle = Text("Cat & Dog People").set_color(YELLOW).shift(3*UP)
        self.play(DrawBorderThenFill(dogchart), FadeIn(dualtitle))
        self.wait(10)
        self.play(Uncreate(catchart), Uncreate(dogchart), Uncreate(dualtitle))

        # hypothesis test explanation scene
        hypttxt = Tex("Two Sample Hypothesis Test for a difference of Means").set_color(YELLOW)
        smpltxt = Tex("$n_{Dog People} > n_{Cat People}$")
        toutline = Rectangle(width=smpltxt.width * 1.2, height=smpltxt.height * 1.35, stroke_color=YELLOW)
        nulltxt = Tex("$H_{0}:$ There is no relationship")
        alttxt = Tex("$H_{a}:$ There is a relationship")
        mhyptxt = Tex("$H_{0}:\\overline{X}_{Cat siblings} = \\overline{X}_{Dog Siblings}$ \\\\ $H_{a}: \\overline{X}_{Cat siblings} \\neq \\overline{X}_{Dog Siblings}$").set_color(BLUE)
        atxt = Tex("$\\alpha = 0.05$").next_to(mhyptxt, DOWN, buff=0.3)
        box = VGroup(smpltxt, toutline).shift(1.6 * UP, 2 * LEFT)
        VGroup(hypttxt, box).arrange(DOWN, buff=0.4).shift(3*UP)
        VGroup(nulltxt, alttxt).arrange(RIGHT, buff=0.5).shift(1.3*UP).set_color(GREEN)
        self.play(Write(hypttxt))
        self.wait(1.5)
        self.play(Write(smpltxt), Create(toutline, run_time=2))
        self.wait(1.5)
        self.play(Write(nulltxt))
        self.wait()
        self.play(Write(alttxt))
        self.wait()
        self.play(Write(mhyptxt))
        self.wait()
        self.play(Write(atxt))
        self.wait()
        self.play(Unwrite(hypttxt), Unwrite(smpltxt), Uncreate(toutline), Unwrite(nulltxt), Unwrite(alttxt), Unwrite(mhyptxt), Unwrite(atxt))
        self.wait(3)

        #t dist graph scene
        ax = NumberPlane(x_range=[-3, 3],x_length=7, y_length=6, y_range = [0, 0.45, 0.1], tips=False, axis_config={"include_numbers": True, "include_ticks": True,}).scale(1.1).shift(1*UP).shift(1.5*RIGHT)

        func = lambda x: t.pdf(x, 30)
        t_dist = ax.plot(func)
        area_left = ax.get_area(t_dist, x_range=[-3, -2]).set_color(RED).set_opacity(0.4)
        area_right = ax.get_area(t_dist, x_range=[2, 3]).set_color(RED).set_opacity(0.4)
        area_middle = ax.get_area(t_dist, x_range=[-2, 2]).set_color(GREEN).set_opacity(0.4)
        area_stat = ax.get_area(t_dist, x_range=[-1.12, -1.15]).set_color(BLUE).set_opacity(0.7)

        key_rects = [Rectangle(width=0.5, height=0.5).set_fill(opacity=1, color=GREEN), Rectangle(width=0.5, height=0.5).set_fill(opacity=1, color=BLUE), Rectangle(width=0.5, height=0.5).set_fill(opacity=1, color=RED)]
        VGroup(*key_rects).arrange(DOWN, buff=1).shift(6*LEFT)

        keys = [Text('= area of acceptance').scale(0.3), Text('= test statistic').scale(0.3), Text('= rejection area').scale(0.3)]
        for i in range(len(key_rects)):
            keys[i].next_to(key_rects[i], buff=0.2)

        self.play(GrowFromEdge(ax, UP))
        self.play(Create(t_dist))
        self.play(Create(area_left), Create(area_right), Create(area_middle), Create(area_stat))
        self.play(*[Create(r) for r in key_rects], *[Write(k) for k in keys])
        self.wait(5)

        area_stat_h = area_stat.copy().scale(1.5).set_color(YELLOW).shift(1.5*UP)
        self.play(FadeTransform(area_stat, area_stat_h), FadeOut(t_dist), FadeOut(ax), FadeOut(area_left), FadeOut(area_right), FadeOut(area_middle), *[FadeOut(r) for r in key_rects], *[FadeOut(k) for k in keys])
        t_text = Text("T = -1.1286").next_to(area_stat_h, buff=0.3)
        self.wait()
        self.play(Write(t_text))

        self.wait(5)
        self.play(Unwrite(t_text))
        self.play(FadeTransform(area_stat_h, area_stat), FadeIn(t_dist), FadeIn(ax), FadeIn(area_left), FadeIn(area_right), FadeIn(area_middle), *[FadeIn(r) for r in key_rects], *[FadeIn(k) for k in keys])
        self.wait()
        area_left_h = area_left.copy().scale(1.5).set_color(YELLOW).shift(1.5 * UP)
        area_right_h = area_right.copy().scale(1.5).set_color(YELLOW).shift(1.5 * UP)
        self.play(FadeTransform(area_left, area_left_h), FadeTransform(area_right, area_right_h),FadeOut(t_dist), FadeOut(ax), FadeOut(area_middle), FadeOut(area_stat),*[FadeOut(r) for r in key_rects],
                  *[FadeOut(k) for k in keys])
        t_text = Tex("$\\alpha/2 = 0.25$").next_to(area_left_h, buff=1)
        self.wait()
        self.play(Write(t_text))
        self.wait(4)
        self.play(Unwrite(t_text))
        self.play(FadeTransform(area_left_h, area_left), FadeTransform(area_right_h, area_right), FadeIn(t_dist), FadeIn(ax), FadeIn(area_stat), FadeIn(area_middle), *[FadeIn(r) for r in key_rects], *[FadeIn(k) for k in keys])

        self.wait()
        area_middle_h = area_middle.copy().set_color(YELLOW).scale(1.05).shift(0.2*DOWN)
        self.play(FadeTransform(area_middle, area_middle_h), FadeOut(t_dist),
                  FadeOut(ax), FadeOut(area_left),
                  FadeOut(area_right), FadeOut(area_stat), *[FadeOut(r) for r in key_rects],
                  *[FadeOut(k) for k in keys])
        t_text = Text("95% area of acceptance").next_to(area_middle_h, DOWN, buff=0.1).scale(0.5)
        self.wait()
        self.play(Write(t_text))
        self.wait()
        self.play(Unwrite(t_text))

        pval = Text("P = 0.268").set_color(YELLOW).scale(2)
        self.play(FadeTransform(area_middle_h, pval, stretch=True))
        self.wait(2)
        pvaleq = Text("0.268 > 0.05").set_color(YELLOW).scale(2)
        self.play(Unwrite(pval))
        self.play(Write(pvaleq))
        self.wait(2)
        conclusion = Tex("Fail to reject $H_{0}$: \\\\ Sibling Count has no statisically significant effect \\\\ on pet preference.").set_color(YELLOW)
        self.play(Unwrite(pvaleq))
        self.play(Write(conclusion))
        self.wait(5)

    # Helper Functions
    def create_graph(self, data, bar_names, y_range, title, x_label, y_label):
        chart = BarChart(
            values=data,
            bar_names=bar_names,
            y_range=y_range
        ).scale(1.2).shift(0.3 * DOWN)
        title_text = Title(title)
        title_text.shift(0 * UP).scale(1)
        x_axislabel = chart.get_x_axis_label(x_label).scale(0.7).shift(1.3 * DOWN).shift(5 * LEFT).set_color(YELLOW)
        y_axislabel = chart.get_y_axis_label(y_label).scale(0.7).shift(3 * LEFT).shift(2.7 * DOWN).set_color(YELLOW)
        return (chart, title_text, x_axislabel, y_axislabel)

    def next_anim(self):
        should_continue = self.current_anim > self.prev_anim
        if should_continue:
            self.prev_anim = self.current_anim
            return True
        return False

    def on_key_press(self, symbol, modifiers):
        from pyglet.window import key as pyglet_key
        if symbol == pyglet_key.SPACE:
            self.current_anim += 1

    def on_mouse_motion(self, point, d_point):
        pass

    def on_mouse_scroll(self, point, offset):
        pass

    def on_mouse_drag(self, point, d_point, buttons, modifiers):
        pass
