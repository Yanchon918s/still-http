export async function onRequestGet({ request, env }) {
  const assetUrl = new URL("/sites.json", request.url);
  const asset = await env.ASSETS.fetch(assetUrl);
  if (!asset.ok) return Response.json({ error: "data unavailable" }, { status: 500 });

  const query = new URL(request.url).searchParams.get("q")?.trim().toLowerCase();
  const sites = await asset.json();
  const results = query
    ? sites.filter((site) =>
        [site.url, site.name, site.note].join(" ").toLowerCase().includes(query),
      )
    : sites;

  return Response.json(results, {
    headers: {
      "Access-Control-Allow-Origin": "*",
      "Cache-Control": "public, max-age=300",
    },
  });
}

export function onRequestOptions() {
  return new Response(null, {
    status: 204,
    headers: {
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "GET, OPTIONS",
    },
  });
}
