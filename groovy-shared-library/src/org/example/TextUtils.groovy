package org.example

class TextUtils {
  static String slugify(String s) {
    return s.toLowerCase()
            .replaceAll(/[^a-z0-9]+/, '-')
            .replaceAll(/(^-|-$)/, '')
  }
}
