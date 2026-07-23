---
name: wordpress-themes
version: 1.0.0
author: Mathias Paulenko Echeverz
description: WordPress theme development standards. Covers theme structure, template hierarchy, custom post types, ACF integration, enqueueing assets, security, and performance best practices.
tags: [wordpress, php, theme, cms, frontend, acf]
role: wordpress-developer
model: any
trigger: When the user mentions WordPress theme development, custom post types, ACF, template hierarchy, wp_enqueue, child themes, or WordPress hooks/filters.
---

# WordPress Theme Development

## 1. Theme Structure

```
my-theme/
  style.css          # Theme metadata + base styles
  index.php          # Fallback template
  functions.php      # Theme setup, hooks, helpers
  screenshot.png     # 1200x900 admin preview
  templates/         # Block theme templates (FSE)
  parts/             # Block theme template parts
  blocks/            # Custom block styles
  inc/               # PHP includes
    setup.php
    custom-post-types.php
    acf-fields.php
  assets/
    css/
    js/
    images/
  languages/         # Translation files
```

## 2. Theme Metadata (`style.css`)

```css
/*
Theme Name: My Custom Theme
Theme URI: https://example.com
Author: Mathias Paulenko Echeverz
Author URI: https://example.com
Description: A clean, performant WordPress theme.
Version: 1.0.0
License: GPL-2.0+
License URI: https://example.com/licenses/gpl-2.0.html
Text Domain: my-theme
Domain Path: /languages
Requires at least: 6.0
Requires PHP: 8.0
*/
```

## 3. Enqueueing Assets

```php
// functions.php
add_action('wp_enqueue_scripts', function () {
    $theme_version = wp_get_theme()->get('Version');
    
    wp_enqueue_style(
        'my-theme-style',
        get_stylesheet_uri(),
        [],
        $theme_version
    );
    
    wp_enqueue_script(
        'my-theme-app',
        get_template_directory_uri() . '/assets/js/app.js',
        [],
        $theme_version,
        true // in_footer
    );
    
    wp_localize_script('my-theme-app', 'themeData', [
        'ajaxUrl' => admin_url('admin-ajax.php'),
        'restUrl' => rest_url(),
        'nonce'   => wp_create_nonce('wp_rest'),
    ]);
});
```

## 4. Template Hierarchy

| Request | Template Used |
|---------|---------------|
| Single post | `single.php` → `singular.php` → `index.php` |
| Page | `page-{slug}.php` → `page-{id}.php` → `page.php` |
| Archive | `archive-{post_type}.php` → `archive.php` |
| Category | `category-{slug}.php` → `category.php` |
| Search | `search.php` |
| 404 | `404.php` |
| Home (blog) | `home.php` → `index.php` |
| Front page | `front-page.php` |

## 5. Custom Post Types

```php
// inc/custom-post-types.php
add_action('init', function () {
    register_post_type('portfolio', [
        'labels'      => [
            'name'          => __('Portfolios', 'my-theme'),
            'singular_name' => __('Portfolio', 'my-theme'),
        ],
        'public'      => true,
        'has_archive' => true,
        'rewrite'     => ['slug' => 'portfolio'],
        'supports'    => ['title', 'editor', 'thumbnail', 'excerpt'],
        'menu_icon'   => 'dashicons-portfolio',
        'show_in_rest' => true, // Gutenberg support
    ]);
});
```

## 6. ACF Integration

```php
// inc/acf-fields.php
if (function_exists('acf_add_local_field_group')) {
    acf_add_local_field_group([
        'key'      => 'group_portfolio_details',
        'title'    => 'Portfolio Details',
        'fields'   => [
            [
                'key'   => 'field_client_name',
                'label' => 'Client Name',
                'name'  => 'client_name',
                'type'  => 'text',
            ],
            [
                'key'   => 'field_project_url',
                'label' => 'Project URL',
                'name'  => 'project_url',
                'type'  => 'url',
            ],
        ],
        'location' => [
            [
                [
                    'param'    => 'post_type',
                    'operator' => '==',
                    'value'    => 'portfolio',
                ],
            ],
        ],
    ]);
}
```

## 7. Security

```php
// Escape all output
<h1><?php echo esc_html(get_the_title()); ?></h1>
<a href="<?php echo esc_url(get_permalink()); ?>">Read more</a>

// Sanitize input
$email = sanitize_email($_POST['email']);

// Nonce verification
if (!wp_verify_nonce($_POST['_wpnonce'], 'my_action')) {
    wp_die('Security check failed');
}

// Prepared queries
$wpdb->get_results(
    $wpdb->prepare("SELECT * FROM {$wpdb->posts} WHERE post_status = %s", 'publish')
);
```

## 8. Performance

- Use `wp_enqueue_*` (no hardcoded `<script>`/`<link>`).
- Enable object caching (Redis/Memcached).
- Optimize images (WebP, lazy loading).
- Minimize autoloaded options.
- Use `get_template_part()` for reusable chunks.
- Enable Gzip and browser caching via server config.

## 9. Translations

```php
// Load text domain
add_action('after_setup_theme', function () {
    load_theme_textdomain('my-theme', get_template_directory() . '/languages');
});

// In templates
_e('Read more', 'my-theme');
$title = __('Latest Posts', 'my-theme');
```
