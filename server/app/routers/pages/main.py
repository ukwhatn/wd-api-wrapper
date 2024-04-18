import wikidot
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from wikidot.common import exceptions

# define router
router = APIRouter(
    tags=["pages"],
)


def get_site(client: wikidot.Client, site_name: str):
    try:
        site = client.site.get(site_name)
    except exceptions.NotFoundException:
        return JSONResponse(status_code=404, content={"status": "error", "message": "site not found"})
    except Exception:
        return JSONResponse(status_code=500, content={"status": "error", "message": "internal server error"})

    return site


class PageSearchCriteria(BaseModel):
    pagetype: str = None
    category: str = None
    tags: str = None
    parent: str = None
    link_to: str = None
    created_at: str = None
    updated_at: str = None
    created_by: str = None
    rating: str = None
    votes: str = None
    name: str = None
    fullname: str = None
    range: str = None
    order: str = None
    offset: int = None
    limit: int = None
    per_page: int = None
    separate: str = None
    wrapper: str = None

    id: bool = False

    def as_dict(self):
        return {k: v for k, v in self.dict().items() if v is not None}


# define route
@router.post("/{site_name}/pages")
def get_pages(
        site_name: str,
        criteria: PageSearchCriteria
):
    parameters = criteria.as_dict()

    is_id_requested = parameters.pop("id", False)

    with wikidot.Client() as client:
        site = get_site(client, site_name)

        if isinstance(site, JSONResponse):
            return site

        pages = site.pages.search(**parameters)
        if is_id_requested:
            pages.get_page_ids()

        res = []
        for page in pages:
            res.append(
                {
                    "id": page.id if is_id_requested else None,
                    "fullname": page.fullname,
                    "name": page.name,
                    "category": page.category,
                    "title": page.title,
                    "children_count": page.children_count,
                    "comments_count": page.comments_count,
                    "size": page.size,
                    "rating": page.rating,
                    "votes_count": page.votes_count,
                    "rating_percent": page.rating_percent,
                    "revisions_count": page.revisions_count,
                    "parent_fullname": page.parent_fullname,
                    "tags": page.tags,
                    "created_by": {
                        "id": page.created_by.id,
                        "name": page.created_by.name,
                        "unix_name": page.created_by.unix_name,
                        "avatar_url": page.created_by.avatar_url,
                        "ip": page.created_by.ip
                    },
                    "created_at": page.created_at,
                    "updated_by": {
                        "id": page.updated_by.id,
                        "name": page.updated_by.name,
                        "unix_name": page.updated_by.unix_name,
                        "avatar_url": page.updated_by.avatar_url,
                        "ip": page.updated_by.ip
                    },
                    "updated_at": page.updated_at,
                    "commented_by": {
                        "id": page.commented_by.id,
                        "name": page.commented_by.name,
                        "unix_name": page.commented_by.unix_name,
                        "avatar_url": page.commented_by.avatar_url,
                        "ip": page.commented_by.ip
                    } if page.commented_by else None,
                    "commented_at": page.commented_at
                }
            )

    return res


@router.get("/{site_name}/pages/{page_fullname}/source")
def get_page_source(
        site_name: str,
        page_fullname: str
):
    with wikidot.Client() as client:
        site = get_site(client, site_name)

        if isinstance(site, JSONResponse):
            return site

        page = site.page.get(page_fullname, raise_when_not_found=False)

        if not page:
            return JSONResponse(status_code=404, content={"status": "error", "message": "page not found"})

        return {
            "source": page.source.wiki_text,
        }


@router.get("/{site_name}/pages/{page_fullname}/revisions")
def get_page_revisions(
        site_name: str,
        page_fullname: str,
        source: bool = False,
        html: bool = False
):
    with wikidot.Client() as client:
        site = get_site(client, site_name)

        if isinstance(site, JSONResponse):
            return site

        page = site.page.get(page_fullname, raise_when_not_found=False)

        if not page:
            return JSONResponse(status_code=404, content={"status": "error", "message": "page not found"})

        revisions = page.revisions

        if source:
            revisions.get_sources()
        if html:
            revisions.get_htmls()

        res = []
        for revision in revisions:
            res.append(
                {
                    "id": revision.id,
                    "rev_no": revision.rev_no,
                    "created_by": {
                        "id": revision.created_by.id,
                        "name": revision.created_by.name,
                        "unix_name": revision.created_by.unix_name,
                        "avatar_url": revision.created_by.avatar_url,
                        "ip": revision.created_by.ip
                    },
                    "created_at": revision.created_at,
                    "comment": revision.comment,
                    "source": revision.source.wiki_text if source else None,
                    "html": revision.html if html else None
                }
            )

    return res
