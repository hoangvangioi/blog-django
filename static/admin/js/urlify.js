/*global XRegExp*/
'use strict';
{
    const VIETNAM_MAP = {
        'á': 'a', 'à': 'a', 'ạ': 'a', 'ả': 'a', 'ã': 'a', 'ă': 'a', 'ắ': 'a', 'ằ': 'a', 'ặ': 'a',
        'ẳ': 'a', 'ẵ': 'a', 'â': 'a', 'ấ': 'a', 'ầ': 'a', 'ậ': 'a', 'ẩ': 'a', 'ẫ': 'a', 'Á': 'a',
        'À': 'a', 'Ạ': 'a', 'Ả': 'a', 'Ã': 'a', 'Ă': 'a', 'Ắ': 'a', 'Ằ': 'a', 'Ặ': 'a', 'Ẳ': 'a',
        'Ẵ': 'a', 'Â': 'a', 'Ấ': 'a', 'Ầ': 'a', 'Ậ': 'a', 'Ẩ': 'a', 'Ẫ': 'a',
        'đ': 'd', 'Đ': 'd',
        'è': 'e', 'é': 'e', 'ẻ': 'e', 'ẽ': 'e', 'ẹ': 'e',
        'ê': 'e', 'ề': 'e', 'ế': 'e', 'ể': 'e', 'ễ': 'e', 'ệ': 'e',
        'È': 'e', 'É': 'e', 'Ẻ': 'e', 'Ẽ': 'e', 'Ẹ': 'e',
        'Ê': 'e', 'Ề': 'e', 'Ế': 'e', 'Ể': 'e', 'Ễ': 'e', 'Ệ': 'e',
        'ì': 'i', 'í': 'i', 'ỉ': 'i', 'ĩ': 'i', 'ị': 'i',
        'Ì': 'i', 'Í': 'i', 'Ỉ': 'i', 'Ĩ': 'i', 'Ị': 'i',
        'ò': 'o', 'ó': 'o', 'ỏ': 'o', 'õ': 'o', 'ọ': 'o',
        'ô': 'o', 'ồ': 'o', 'ố': 'o', 'ổ': 'o', 'ỗ': 'o', 'ộ': 'o',
        'ơ': 'o', 'ờ': 'o', 'ớ': 'o', 'ở': 'o', 'ỡ': 'o', 'ợ': 'o',
        'Ò': 'o', 'Ó': 'o', 'Ỏ': 'o', 'Õ': 'o', 'Ọ': 'o',
        'Ô': 'o', 'Ồ': 'o', 'Ố': 'o', 'Ổ': 'o', 'Ỗ': 'o', 'Ộ': 'o',
        'Ơ': 'o', 'Ờ': 'o', 'Ớ': 'o', 'Ở': 'o', 'Ỡ': 'o', 'Ợ': 'o',
        'ù': 'u', 'ú': 'u', 'ủ': 'u', 'ũ': 'u', 'ụ': 'u',
        'ư': 'u', 'ừ': 'u', 'ứ': 'u', 'ử': 'u', 'ữ': 'u', 'ự': 'u',
        'Ù': 'u', 'Ú': 'u', 'Ủ': 'u', 'Ũ': 'u', 'Ụ': 'u',
        'Ư': 'u', 'Ừ': 'u', 'Ứ': 'u', 'Ử': 'u', 'Ữ': 'u', 'Ự': 'u',
        'ỳ': 'y', 'ý': 'y', 'ỷ': 'y', 'ỹ': 'y', 'ỵ': 'y',
        'Y': 'y', 'Ỳ': 'y', 'Ý': 'y', 'Ỷ': 'y', 'Ỹ': 'y', 'Ỵ': 'y'
    };

    const ALL_DOWNCODE_MAPS = [
        VIETNAM_MAP,
    ];

    const Downcoder = {
        'Initialize': function() {
            if (Downcoder.map) { // already made
                return;
            }
            Downcoder.map = {};
            for (const lookup of ALL_DOWNCODE_MAPS) {
                Object.assign(Downcoder.map, lookup);
            }
            Downcoder.regex = new RegExp(Object.keys(Downcoder.map).join('|'), 'g');
        }
    };

    function downcode(slug) {
        Downcoder.Initialize();
        return slug.replace(Downcoder.regex, function(m) {
            return Downcoder.map[m];
        });
    }


    function URLify(s, num_chars, allowUnicode) {
        // changes, e.g., "Petty theft" to "petty-theft"
        if (!allowUnicode) {
            s = downcode(s);
        }
        s = s.toLowerCase(); // convert to lowercase
        // if downcode doesn't hit, the char will be stripped here
        if (allowUnicode) {
            // Keep Unicode letters including both lowercase and uppercase
            // characters, whitespace, and dash; remove other characters.
            s = XRegExp.replace(s, XRegExp('[^-_\\p{L}\\p{N}\\s]', 'g'), '');
        } else {
            s = s.replace(/[^-\w\s]/g, ''); // remove unneeded chars
        }
        s = s.replace(/^\s+|\s+$/g, ''); // trim leading/trailing spaces
        s = s.replace(/[-\s]+/g, '-'); // convert spaces to hyphens
        s = s.substring(0, num_chars); // trim to first num_chars chars
        s = s.replace(/-+$/g, ''); // trim any trailing hyphens
        return s;
    }
    window.URLify = URLify;
}
