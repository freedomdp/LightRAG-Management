# WordPress SEO: Code-First Approach (No Plugins)

This document outlines the professional "Pure Code" approach to SEO on WordPress, eliminating the need for heavy plugins like Yoast or Rank Math while maintaining full control over the technical architecture.

## 1. Direct Title Management

The standard `pre_get_document_title` filter allows precise control over page titles.

```php
/**
 * Advanced Custom SEO Title Logic
 * Integration with ACF (Advanced Custom Fields)
 */
add_filter('pre_get_document_title', 'antigravity_custom_seo_title', 15);
function antigravity_custom_seo_title($title) {
    if (is_home() || is_front_page()) {
        return get_bloginfo('name') . ' | ' . get_bloginfo('description');
    }

    if (is_category()) {
        $term_id = get_queried_object()->term_id;
        $acf_title = get_field('seo_title', 'category_' . $term_id);
        return $acf_title ? $acf_title : $title;
    }

    if (is_single() || is_page()) {
        $acf_title = get_field('seo_title');
        return $acf_title ? $acf_title : $title;
    }

    return $title;
}
```

## 2. Technical Head Cleanup

Reducing the "bloat" in `<head>` improves security and crawlability.

```php
/**
 * Remove Unnecessary WP Head Elements
 */
function antigravity_technical_cleanup() {
    // Security & Versioning
    remove_action('wp_head', 'wp_generator'); // Removes WP version
    remove_action('wp_head', 'rsd_link');    // Removes EditURI link
    remove_action('wp_head', 'wlwmanifest_link'); // Removes Windows Live Writer link

    // Feeds & API
    remove_action('wp_head', 'feed_links', 2);
    remove_action('wp_head', 'feed_links_extra', 3);
    remove_action('wp_head', 'rest_output_link_wp_head'); // Removes REST API link

    // Emojis (SEO & Performance)
    remove_action('wp_head', 'print_emoji_detection_script', 7);
    remove_action('wp_print_styles', 'print_emoji_styles');
}
add_action('init', 'antigravity_technical_cleanup');
```

## 3. Automated SEO Factors

### Automatic Alt Tags from Title
If an image misses an alt tag, dynamically use the item title.

```php
add_filter('wp_get_attachment_image_attributes', 'antigravity_auto_alt_tag', 10, 2);
function antigravity_auto_alt_tag($attr, $attachment) {
    if (empty($attr['alt'])) {
        $attr['alt'] = get_the_title($attachment->ID);
    }
    return $attr;
}
```

### Robots.txt via Code
Manage indexing directly in `functions.php`.

```php
add_filter('robots_txt', 'antigravity_custom_robots', 10, 2);
function antigravity_custom_robots($output, $public) {
    $output .= "Disallow: /wp-admin/\n";
    $output .= "Disallow: /wp-includes/\n";
    $output .= "Disallow: /?s=\n";
    $output .= "Sitemap: " . home_url('/sitemap_index.xml') . "\n";
    return $output;
}
```

## 4. Why Use Code Over Plugins?

> [!IMPORTANT]
> - **Performance**: Plugins like Rank Math load dozens of files and database queries on every page load.
> - **Maintenance**: No need for updates that might break the design.
> - **Security**: Fewer plugins mean a smaller attack surface.
> - **Customization**: Direct integration with specific themes/ACF logic.

## 5. Strategic Rule for Agents

If a project requires advanced SEO (Schema, Redirects), first attempt implementation via `functions.php`. Only suggest a plugin if the logic becomes too complex for sustainable code maintenance (e.g., highly complex Redirection systems or massive multisite setups).
