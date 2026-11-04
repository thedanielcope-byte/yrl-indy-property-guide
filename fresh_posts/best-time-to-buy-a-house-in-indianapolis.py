"""Best Time to Buy a House in Indianapolis, month by month (Nov 2026).

Every market figure is from MIBOR's own monthly report for that month (17-county MIBOR BLC
service area, single-family homes), read from the PDFs in MIBOR's report archive on Nov 3
2026. Each month's numbers come from that month's report as first published (MIBOR revises
slightly in later reports). July and August 2026 closed-sale counts appear only in chart
images, so they show as n/a. Dec 2025, Jan 2026 and Jun 2026 match the winter buying post.
2025 pattern: Jan 2025 median $292,000 (Jan 2025 report), $325,000 in June and July 2025
(June and July 2025 reports).

Mortgage rates: Freddie Mac PMMS history file. 52 weeks to Oct 29 2026: low 5.98% (Feb 26
2026), high 7.40% (Oct 8 and Oct 15 2026), latest 7.24% (Oct 29 2026), 6.17% a year earlier
(Oct 30 2025). February 2026 weekly average 6.05%. Payment math (ours): 30-year P&I, 10% down.
On a $310,000 home: $1,682/mo at 6.05% vs $1,901 at 7.24% (+$220). At 7.24%, $300,000 vs
$330,000 = +$184/mo.
"""

M = "https://www.mibor.com/wp-content/uploads/"
ARCHIVE = "https://www.mibor.com/buyers-sellers/market-insights/market-insights-report-archive/"

ROWS = [
 ("Oct 2025", "2,649", "$315,000", "24", "97.5%", "6,432", "2.4"),
 ("Nov 2025", "2,162", "$312,000", "30", "97.5%", "6,010", "2.8"),
 ("Dec 2025", "2,414", "$310,000", "41", "97.5%", "5,254", "2.2"),
 ("Jan 2026", "1,475", "$300,000", "50", "97%", "4,878", "3.3"),
 ("Feb 2026", "1,874", "$299,000", "33", "97.3%", "4,622", "2.5"),
 ("Mar 2026", "2,394", "$310,000", "17", "98%", "4,816", "2.0"),
 ("Apr 2026", "2,672", "$316,000", "12", "98.5%", "5,327", "2.0"),
 ("May 2026", "3,233", "$325,000", "12", "98.6%", "5,747", "1.8"),
 ("Jun 2026", "3,342", "$330,000", "15", "98.7%", "6,197", "1.9"),
 ("Jul 2026", "n/a", "$330,000", "20", "98.4%", "6,769", "2.2"),
 ("Aug 2026", "n/a", "$327,250", "23", "98.2%", "6,941", "2.5"),
 ("Sep 2026", "2,549", "$320,000", "27", "98.1%", "7,405", "2.9"),
]

TABLE = ("\n".join(f" <tr><td>{m}</td><td>{c}</td><td>{p}</td><td>{d}</td><td>{a}</td><td>{l}</td><td>{s}</td></tr>"
                   for m, c, p, d, a, l, s in ROWS))

POST = dict(
 slug="best-time-to-buy-a-house-in-indianapolis",
 title="Best Time to Buy a House in Indianapolis (Month by Month)",
 headline="Best Time to Buy a House in Indianapolis, Month by Month",
 h1_html="Best Time to Buy a House in Indianapolis: <em>Month by Month</em>",
 desc=("When is the best time to buy a house in Indianapolis? A year of MIBOR data on prices, competition and "
       "selection, month by month, plus why rates can matter more."),
 date="2026-11-03", month="November 2026",
 category="Buying a Home", eyebrow="BUYING A HOME",
 focus="best time to buy a house in indianapolis",
 hero_sub="Twelve months of MIBOR data on prices, days on market and homes for sale, what it means for when you buy, and why your mortgage rate can matter more than the month.",
 badges=["Buying a Home", "Market Data", "Central Indiana"],
 read_min=7,
 card_title="Best Time to Buy a House in Indy",
 card_sub="A year of MIBOR data, month by month, and what it means for buyers.",
 qa_heading="Best Time to Buy at a Glance",
 qa_lead=("<strong>When is the best time to buy a house in Indianapolis?</strong> For the most negotiating room, late fall "
          "and winter. Across MIBOR&rsquo;s 17-county area, homes that sold in January 2026 took a median of 50 days and went "
          "for 97% of asking, versus 12 days and 98.6% in May, and median prices were lowest in January and February. "
          "The catch is fewer homes to choose from. Spring and early summer bring the most competition and the highest prices."),
 qa_facts=[
  ("Lowest median price", "$299,000 (Feb 2026)"),
  ("Highest median price", "$330,000 (Jun and Jul 2026)"),
  ("Slowest sales", "50-day median (Jan 2026)"),
  ("Fastest sales", "12-day median (Apr and May 2026)"),
  ("Most homes for sale", "7,405 (Sep 2026)"),
  ("30-year mortgage rate", "7.24% (Oct 29, 2026)"),
 ],
 toc=[("month-by-month", "The Year, Month by Month"), ("cheapest", "When Homes Cost the Least"),
      ("leverage", "When Buyers Have the Most Leverage"), ("selection", "The Trade-Off: Selection"),
      ("rates", "Rates Can Matter More Than the Month"), ("your-situation", "The Best Time for Your Situation"),
      ("our-take", "Our Take")],
 body=f"""
 <p>&ldquo;When should we buy?&rdquo; is one of the first questions we hear, and the honest answer depends on what you care about most: price, competition, choice or your monthly payment. The Central Indiana market has a clear seasonal rhythm, so here is a full year of MIBOR&rsquo;s own numbers, month by month, and what they mean for when you shop. If you&rsquo;re already leaning toward the colder months, our guide to <a href="/blog/buying-a-house-in-winter-indianapolis/">buying a house in winter in Indianapolis</a> covers inspections and year-end closings in detail.</p>

 <h2 id="month-by-month">The Indianapolis Market, Month by Month</h2>
 <p>MIBOR REALTOR&reg; Association reports on single-family homes across its 17-county Central Indiana service area every month. These are the figures from each month&rsquo;s report for the most recent full year:</p>
 <div style="overflow-x:auto;">
 <table class="data-table">
 <thead><tr><th>Month</th><th>Closed sales</th><th>Median price</th><th>Median days on market</th><th>Share of asking</th><th>Homes for sale</th><th>Months of supply</th></tr></thead>
 <tbody>
{TABLE}
 </tbody>
 </table>
 </div>
 <p style="font-size:.88rem;color:var(--gray);">Source: MIBOR monthly market reports, October 2025 to September 2026, single-family homes. MIBOR&rsquo;s July and August 2026 reports give the change in closed sales but not the count, so those cells are blank. MIBOR sometimes revises a month slightly in later reports; these are the figures as each month was first published.</p>
 <p>The pattern is easy to see. Sales and prices climb through spring, homes sell fastest in April and May, prices top out in June and July, and then everything cools: by January, sales are at their lowest, homes take the longest to sell and buyers pay the smallest share of the asking price.</p>

 <h2 id="cheapest">When Homes Cost the Least</h2>
 <p>On median price alone, the cheapest months were <strong>January and February</strong>: $300,000 in January 2026 and $299,000 in February, compared with <strong>$330,000</strong> in June and July. The same thing happened the year before, when the median went from $292,000 in January 2025 to $325,000 in June and July 2025.</p>
 <p>One caution: a median reflects the mix of homes that sell that month. Larger, pricier homes tend to sell in spring and summer, when families want to move between school years, so part of that roughly 10% gap is about which homes sell, not a discount on the same house. A particular home won&rsquo;t necessarily cost 10% less in January. But less competition does give you more room to negotiate on price, repairs or closing costs.</p>

 <h2 id="leverage">When Buyers Have the Most Leverage</h2>
 <p>Two numbers show who has the upper hand: how long homes sit, and how close to asking price they sell.</p>
 <ul>
 <li><strong>Winter (December to February):</strong> a median of 33 to 50 days on market and 97% to 97.5% of asking price. January 2026 had a 3.3-month supply, the highest of the year, which is the most balanced the market got.</li>
 <li><strong>Spring (April and May):</strong> a 12-day median and 98.5% to 98.6% of asking. Well-priced homes often draw several offers within days, which is when our tips on <a href="/blog/how-to-win-a-bidding-war-in-indianapolis/">winning a bidding war</a> matter most.</li>
 <li><strong>Fall (September to November):</strong> homes start to sit again (27 days in September 2026, 30 in November 2025) and the share of asking slips back toward 97.5%.</li>
 </ul>
 <p>Fall also stood out in 2026 for a different reason: September had <strong>7,405</strong> single-family homes for sale, the most of any month in the table, while the median home took 27 days to sell. More homes to choose from and less pressure to decide on the spot made early fall one of the better windows for buyers this year.</p>

 <h2 id="selection">The Trade-Off: Fewer Homes to Choose From</h2>
 <p>The months with the most leverage also have the least selection. Homes for sale bottomed out at 4,622 in February 2026, about 38% fewer than September&rsquo;s 7,405, because new listings drop off around the holidays. If you need a specific school district, a big lot or a ranch with a basement, a thin winter market may not have it, and you may need to be ready to move quickly when the right home appears. Spring brings the most new listings, but also the most buyers chasing them.</p>

 <h2 id="rates">Mortgage Rates Can Matter More Than the Month</h2>
 <p>Seasonal price swings get the attention, but your mortgage rate often moves your payment more. Freddie Mac&rsquo;s average 30-year fixed rate was <strong>7.24%</strong> on October 29, 2026. Over the previous 52 weeks it ran from a low of <strong>5.98%</strong> (February 26, 2026) to a high of <strong>7.40%</strong> (October 8 and 15, 2026); a year earlier it was 6.17%.</p>
 <p>Here&rsquo;s what that means in dollars, using our own math on a 30-year loan with 10% down:</p>
 <ul>
 <li>On a $310,000 home, February 2026&rsquo;s average rate (6.05%) meant about <strong>$1,682 a month</strong> in principal and interest. At 7.24%, the same home costs about <strong>$1,901</strong>, roughly $220 more every month.</li>
 <li>At 7.24%, the gap between a $300,000 home and a $330,000 home, the size of the winter-to-summer swing in median prices, is about <strong>$184 a month</strong>.</li>
 </ul>
 <p>In other words, a rate move of about one point can outweigh the whole seasonal price swing. Nobody can reliably predict rates, so we don&rsquo;t recommend waiting for a perfect month. Buy when the home and the payment work for you, and if rates drop later, refinancing may be an option. See <a href="/blog/how-much-house-can-i-afford-indianapolis/">how much house you can afford in Indianapolis</a> at today&rsquo;s rates, or run your own numbers with our <a href="/services/mortgages/">mortgage calculator</a>.</p>

 <h2 id="your-situation">The Best Time for Your Situation</h2>
 <h3>First-time buyers</h3>
 <p>Late fall and winter can be a good fit: fewer competing offers, more time to think, and more room to ask for help with closing costs. Get <a href="/blog/pre-approval-vs-pre-qualification-indianapolis/">pre-approved</a> before you start, and check whether you qualify for <a href="/blog/down-payment-assistance-programs-in-indiana-2026/">down payment assistance in Indiana</a>, which can matter more than the month.</p>
 <h3>Relocating buyers</h3>
 <p>Your start date usually picks the month for you. If you have flexibility, early fall combines the widest selection with less pressure, and a winter purchase often means calmer negotiations. Our <a href="/services/relocation-buyers/">relocation team</a> runs <a href="/blog/relocating-to-indianapolis-virtual-home-tours/">live video tours</a> so you can shop before you arrive.</p>
 <h3>Move-up buyers who need to sell first</h3>
 <p>You&rsquo;re on both sides of the season. Spring is the strongest time to sell (a 12-day median and 98.6% of asking in May 2026), but it&rsquo;s also the most competitive time to buy. Common ways to bridge the gap include a <a href="/glossary/home-sale-contingency/">home sale contingency</a>, a longer closing or a short rent-back on the home you sell, or <a href="/blog/using-home-equity-to-buy-your-next-home-indianapolis/">using your equity</a> to buy before you sell. Our <a href="/services/move-up-buyers/">move-up buyer</a> page walks through the options, and the <a href="/blog/selling-a-house-in-winter-indianapolis/">winter selling guide</a> covers listing when it&rsquo;s cold.</p>

 <h2 id="our-take">Our Take</h2>
 <p>If you want the most leverage, shop from October through February. If you want the most choice, early fall was the sweet spot in 2026. If you want the most homes coming on the market and can handle competition, spring is busiest. Whatever the month, your rate, budget and readiness usually matter more than the calendar. A typical financed purchase takes about 30 to 45 days to close (here&rsquo;s <a href="/blog/how-long-does-it-take-to-close-on-a-house-in-indiana/">how the timeline works</a>), so start a couple of months before you want to move. For the latest numbers, see our <a href="/market-updates/">monthly market updates</a> and the <a href="/blog/indianapolis-market-update-october-2026/">October 2026 update</a>. Ready to look? <a href="/search/">Search homes for sale</a> or <a href="/schedule/">book a call with our team</a>.</p>
""",
 faqs=[
  ("What is the best month to buy a house in Indianapolis?",
   "It depends on what matters most to you. For negotiating room, January stood out: in MIBOR's 17-county area, homes that sold in January 2026 took a median of 50 days and sold for 97% of asking, with a 3.3-month supply. For selection, September 2026 had the most homes for sale (7,405). April and May are the most competitive months, with a 12-day median."),
  ("When are house prices lowest in Indianapolis?",
   "Median sale prices are usually lowest in January and February. MIBOR reported a $300,000 median in January 2026 and $299,000 in February, compared with $330,000 in June and July 2026. The same pattern showed up in 2025 ($292,000 in January, $325,000 in June and July). Part of the gap reflects which homes sell each season, not a discount on the same home."),
  ("Is it better to buy a house in spring or winter in Indianapolis?",
   "Winter usually offers less competition and more room to negotiate, but fewer homes to choose from. Spring offers more new listings but more buyers too: homes sold in a median of 12 days in April and May 2026, compared with 50 days in January 2026. If you need a specific type of home, spring's selection may matter more; if you want leverage, winter is better."),
  ("Do mortgage rates matter more than the time of year?",
   "Often, yes. Freddie Mac's 30-year rate ranged from 5.98% to 7.40% in the 52 weeks to October 29, 2026. On a $310,000 home with 10% down, the difference between 6.05% and 7.24% is about $220 a month in principal and interest, more than the roughly $184 a month separating a $300,000 and a $330,000 home at 7.24%."),
  ("Should I wait until spring to buy a house?",
   "Only if you need the wider selection spring brings or your timeline is flexible. Waiting means more competition and, based on the last two years, higher median prices, and nobody can predict where rates will be. If you find the right home at a payment you're comfortable with, buying in fall or winter can mean a calmer negotiation."),
  ("How far ahead should I start looking if I want to move by summer?",
   "Start two to three months before you want to move. Get pre-approved first, allow a few weeks to find the right home, and plan on about 30 to 45 days from accepted offer to closing for a financed purchase. In spring, homes can go under contract within days, so be ready to act quickly."),
 ],
 sources=[
  ("MIBOR market report archive (all months cited)", ARCHIVE),
  ("MIBOR, October 2025", M + "2025/11/MIBOR-Market-Insights-Report-2025_10.pdf"),
  ("MIBOR, January 2026", M + "2026/02/MIBOR-Market-Insights-Report-January_2026.pdf"),
  ("MIBOR, February 2026", M + "2026/03/MIBOR-Monthly-Market-Report_Feb-26.pdf"),
  ("MIBOR, May 2026", M + "2026/06/MIBOR-Monthly-Market-Report-May.pdf"),
  ("MIBOR, June 2026", M + "2026/07/MIBOR-Monthly-Market-Report-June.pdf"),
  ("MIBOR, September 2026", M + "2026/10/MIBOR-Monthly-Market-Report-September.pdf"),
  ("MIBOR, January 2025", M + "2025/06/MIBOR-Market-Insights-Report-2025_01.pdf"),
  ("MIBOR, June 2025", M + "2025/07/MIBOR-Market-Insights-Report-June_2025-1.pdf"),
  ("Freddie Mac Primary Mortgage Market Survey", "https://www.freddiemac.com/pmms"),
  ("Freddie Mac PMMS weekly history", "https://www.freddiemac.com/pmms/docs/PMMS_history.csv"),
 ],
 related=[
  ("/blog/buying-a-house-in-winter-indianapolis/", "Buying a House in Winter in Indianapolis"),
  ("/blog/how-much-house-can-i-afford-indianapolis/", "How Much House Can I Afford in Indianapolis?"),
  ("/market-updates/", "Indianapolis Market Updates"),
 ],
 cta=("Ready to Time Your Move?",
      "We&rsquo;ll show you what&rsquo;s for sale right now, what similar homes have sold for, and how today&rsquo;s market fits your timeline and budget.",
      [("/search/", "Search Homes for Sale →", "btn-white"),
       ("/schedule/", "Book a Call With Our Team", "btn-outline")]),
 resources=[
  ("/services/buyer-representation/", "Buyer Representation"),
  ("/blog/making-a-winning-offer-on-a-home-indianapolis/", "Making a Winning Offer"),
  ("/blog/pre-approval-vs-pre-qualification-indianapolis/", "Pre-Approval vs. Pre-Qualification"),
  ("/services/mortgages/", "Mortgage Calculator"),
 ],
 link_from=[
  ("blog/buying-a-house-in-winter-indianapolis/index.html",
   'Comparing winter with the rest of the year? See <a href="/blog/best-time-to-buy-a-house-in-indianapolis/">the best time to buy a house in Indianapolis, month by month</a>, with a full year of MIBOR data.'),
  ("blog/first-time-home-buyer-guide-indianapolis-2026/index.html",
   'Wondering when to start shopping? Our <a href="/blog/best-time-to-buy-a-house-in-indianapolis/">month-by-month look at the best time to buy in Indianapolis</a> shows when prices, competition and selection peak.'),
 ],
 about={"@type": "City", "name": "Indianapolis", "containedInPlace": {"@type": "State", "name": "Indiana"}},
)
