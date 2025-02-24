import katex from 'katex';

<<<<<<< HEAD
=======
const DELIMITER_LIST = [
	{ left: '$$', right: '$$', display: true },
	{ left: '$', right: '$', display: false },
	{ left: '\\pu{', right: '}', display: false },
	{ left: '\\ce{', right: '}', display: false },
	{ left: '\\(', right: '\\)', display: false },
	{ left: '\\[', right: '\\]', display: true },
	{ left: '\\begin{equation}', right: '\\end{equation}', display: true }
];

// const DELIMITER_LIST = [
//     { left: '$$', right: '$$', display: false },
//     { left: '$', right: '$', display: false },
// ];

// const inlineRule = /^(\${1,2})(?!\$)((?:\\.|[^\\\n])*?(?:\\.|[^\\\n\$]))\1(?=[\s?!\.,:？！。，：]|$)/;
// const blockRule = /^(\${1,2})\n((?:\\[^]|[^\\])+?)\n\1(?:\n|$)/;

let inlinePatterns = [];
let blockPatterns = [];

function escapeRegex(string) {
	return string.replace(/[-\/\\^$*+?.()|[\]{}]/g, '\\$&');
}

function generateRegexRules(delimiters) {
	delimiters.forEach((delimiter) => {
		const { left, right, display } = delimiter;
		// Ensure regex-safe delimiters
		const escapedLeft = escapeRegex(left);
		const escapedRight = escapeRegex(right);

		if (!display) {
			// For inline delimiters, we match everything
			inlinePatterns.push(`${escapedLeft}((?:\\\\[^]|[^\\\\])+?)${escapedRight}`);
		} else {
			// Block delimiters doubles as inline delimiters when not followed by a newline
			inlinePatterns.push(`${escapedLeft}(?!\\n)((?:\\\\[^]|[^\\\\])+?)(?!\\n)${escapedRight}`);
			blockPatterns.push(`${escapedLeft}\\n((?:\\\\[^]|[^\\\\])+?)\\n${escapedRight}`);
		}
	});

	// Math formulas can end in special characters
	const inlineRule = new RegExp(
		`^(${inlinePatterns.join('|')})(?=[\\s?。，!-\/:-@[-\`{-~]|$)`,
		'u'
	);
	const blockRule = new RegExp(`^(${blockPatterns.join('|')})(?=[\\s?。，!-\/:-@[-\`{-~]|$)`, 'u');

	return { inlineRule, blockRule };
}

const { inlineRule, blockRule } = generateRegexRules(DELIMITER_LIST);

>>>>>>> upstream/main
export default function (options = {}) {
	return {
		extensions: [inlineKatex(options, createRenderer(options))]
	};
}

function createRenderer(options) {
	return (token) =>
		katex.renderToString(token.text, { ...options, displayMode: token.displayMode });
}

function inlineKatex(options, renderer) {
	return {
		name: 'inlineKatex',
		level: 'inline',
		start(src: string) {
			return src.indexOf('$');
		},
		tokenizer(src, tokens) {
<<<<<<< HEAD
			const match = src.match(/^\$+([^$\n]+?)\$+/);
=======
			return katexTokenizer(src, tokens, false);
		},
		renderer(token) {
			return `${token?.text ?? ''}`;
		}
	};
}
>>>>>>> upstream/main

			if (match) {
				return {
					type: 'inlineKatex',
					raw: match[0],
					text: match[1].trim(),
					displayMode: match[0].startsWith('$$')
				};
			}
		},
<<<<<<< HEAD
		renderer
=======
		tokenizer(src, tokens) {
			return katexTokenizer(src, tokens, true);
		},
		renderer(token) {
			return `${token?.text ?? ''}`;
		}
>>>>>>> upstream/main
	};
}
