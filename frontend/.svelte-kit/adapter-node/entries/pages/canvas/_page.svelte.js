import { i as head, d as attr, K as ensure_array_like, e as escape_html } from "../../../chunks/index2.js";
function _page($$payload) {
  let accessToken = "";
  let courses = [];
  head($$payload, ($$payload2) => {
    $$payload2.title = `<title>Canvas</title>`;
    $$payload2.out.push(`<meta name="description" content="Link Canvas Account"/>`);
  });
  $$payload.out.push(`<div class="text-column" style="text-align: center;"><h1>Link Canvas account</h1> <label for="accessToken">Enter Canvas Access Token:</label> <input style="width: auto;" type="text"${attr("value", accessToken)}/><br/> <button style="margin: 1rem 0; padding: 0.75rem 1.5rem; font-size: 1.1rem;">Link Canvas Account</button> `);
  {
    $$payload.out.push("<!--[!-->");
  }
  $$payload.out.push(`<!--]--> `);
  if (courses.length) {
    $$payload.out.push("<!--[-->");
    const each_array = ensure_array_like(courses);
    $$payload.out.push(`<h2>Your Courses:</h2> <ul><!--[-->`);
    for (let $$index = 0, $$length = each_array.length; $$index < $$length; $$index++) {
      let course = each_array[$$index];
      $$payload.out.push(`<li>${escape_html(course.name)}</li>`);
    }
    $$payload.out.push(`<!--]--></ul>`);
  } else {
    $$payload.out.push("<!--[!-->");
  }
  $$payload.out.push(`<!--]--></div>`);
}
export {
  _page as default
};
