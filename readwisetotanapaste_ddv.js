// Name: Grab Readwise Highlights

import "@johnlindquist/kit"

let API_TOKEN = await env("TANA_API_TOKEN")
let HIGHLIGHTS_URL = "https://readwise.io/api/v2/export/"

// Credit to: https://github.com/tanainc/tana-paste-examples
// Copy/pasted and refactored to Script Kit: scriptkit.com

let getItemsFromReadwise = async (daysToFetch = 1) => {
  let dateOffset = 24 * 60 * 60 * 1000 * daysToFetch
  let updatedAfterDate = new Date()
  updatedAfterDate.setTime(
    updatedAfterDate.getTime() - dateOffset
  )

  let response = await fetch(
    `${HIGHLIGHTS_URL}?updatedAfter=${updatedAfterDate.toISOString()}`,
    {
      headers: {
        Authorization: `Token ${API_TOKEN}`,
      },
    }
  )
  return await response.json()
}

let daysToFetch = await arg("Days to fetch")
let { results } = await getItemsFromReadwise(
  parseInt(daysToFetch, 10)
)

let result = results.map(book => {
  let isValidSourceURL =
    book.source_url?.startsWith("https://")
  let hasHighlights = book.highlights?.length > 0

  let title = `${book.title}`
  let url = ``
  if (isValidSourceURL) {
    url = `Source URL:: ${book.source_url}`
  }
  let type = `Readwise category:: ${book.category?.replace(/s$/, "")}`

  let author = `Author:: ${book.author}`

  let highlights = book.highlights.map(highlight => {
    let lines = highlight.text.split("\n")
    let cleanLines = lines.map(line => {
      let cleanedLine = line.replace(/•\s+/, "").trim()
      return `${cleanedLine}`
    })

    let note = ``

    if (highlight.note) {
      note = `${highlight.note}`
    }

    return `
${cleanLines}   

${note}
    `.trim()
  })

  let maybeUrl = url
    ? `
    - ${url}
`
    : ``

  let maybeHighlights = highlights?.length
    ? `
    - Highlights
        - ${highlights.join("\n")}`
    : ``

  return `
- Rw ${title} #referenceNote
${maybeUrl}
    - ${type}
    - ${author}
${maybeHighlights} #highlight   
  `.trim()
})

// because I'm on a trial account (I assume)
let [skip, ...rest] = result

// copies the readwise content to the clipboard
// I'm using slice to only take 2 results for demo purposes
await copy(`%%tana%%

${rest.join("\n")}
`)

