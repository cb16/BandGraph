package crawler;

import java.net.MalformedURLException;
import java.net.URL;
import java.util.HashSet;
import java.util.LinkedList;
import java.util.Set;

public class Crawler implements ICrawler {

	//constants
	public final long timeInterval = 10;
	
	//attributes
	public LinkedList<String> queue;

	public Set<String> visitedUrls;

	public String host;

	public long lastVisit;

	public Crawler(String seed) {
		this.queue = new LinkedList<String>();
		this.queue.add(seed);
		this.visitedUrls = new HashSet<String>();
		this.lastVisit = 0;
	}

	//main
	public void crawl() {
		while(!this.queue.isEmpty()) {
			long now = System.currentTimeMillis();
			if(canVisit(now)) {
				String url = this.queue.poll();
				visit(url);
			}
		}
	}

	//visit
	public void visit(String url) {
		
	}

	//utils
	public boolean canVisit(long time) {
		if(time - this.lastVisit > this.timeInterval)
			return true;
		return false;
	}
	
	public boolean isValidUrl(String url) {
		URL urlObj = null;
		try {
			urlObj = new URL(url);
		} catch (MalformedURLException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
			return false;
		}
		return true;
	}

	public String getUrlHost(String url) throws MalformedURLException {
		if(isValidUrl(url))
			return (new URL(url)).getHost();
		return "";
	}

}
