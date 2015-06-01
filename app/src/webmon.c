/* 
   app/src/webmon.c
   :copyright: (c) 2015 by Aravinda VK <mail@aravindavk.in>
   :license: MIT, see LICENSE for more details.
 */
#include <pebble.h>

static Window *s_main_window;
static TextLayer *s_text_layer;

static void window_load(Window *window) {
	Layer *window_layer = window_get_root_layer(window);
	/*GRect bounds = layer_get_bounds(window_layer);*/

	s_text_layer = text_layer_create(GRect(0, 10, 144, 168));
	text_layer_set_text_alignment(s_text_layer, GTextAlignmentCenter);
	text_layer_set_overflow_mode(s_text_layer, GTextOverflowModeWordWrap);
	text_layer_set_font(s_text_layer, fonts_get_system_font(FONT_KEY_GOTHIC_18_BOLD));
	text_layer_set_text_color(s_text_layer, GColorWhite);
	text_layer_set_background_color(s_text_layer, GColorClear);
	text_layer_set_text(s_text_layer, "WEBMON - Open APP CONFIG and add the website URL you want to track");
	layer_add_child(window_layer, text_layer_get_layer(s_text_layer));
}

static void window_unload(Window *window) {
	text_layer_destroy(s_text_layer);
}

static void init() {
	s_main_window = window_create();
	window_set_background_color(s_main_window, COLOR_FALLBACK(GColorFolly, GColorBlack));
	window_set_window_handlers(s_main_window, (WindowHandlers) {
			.load = window_load,
				.unload = window_unload,
				});
	window_stack_push(s_main_window, true);
}

static void deinit() {
	window_destroy(s_main_window);
}

int main() {
	init();
	app_event_loop();
	deinit();
}
